from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from math import ceil, floor
from typing import Any, Callable, Protocol

from vsaa import Nnedi3
from vskernels import Catrom, Kernel, KernelT, Scaler, ScalerT
from vstools import F_VD, KwargsT, MatrixT, fallback, get_w, mod2, plane, vs

from .types import Resolution

__all__ = [
    'GenericScaler',
    'scale_var_clip',
    'fdescale_args'
]


class _GeneriScaleNoShift(Protocol):
    def __call__(self, clip: vs.VideoNode, width: int, height: int, *args: Any, **kwds: Any) -> vs.VideoNode:
        ...


class _GeneriScaleWithShift(Protocol):
    def __call__(
        self, clip: vs.VideoNode, width: int, height: int, shift: tuple[float, float],
        *args: Any, **kwds: Any
    ) -> vs.VideoNode:
        ...


@dataclass
class GenericScaler(Scaler):
    """
    Generic Scaler base class.
    Inherit from this to create more complex scalers with built-in utils.
    Instantiate with a callable taking at least a VideoNode, width, and height
    to use that as a Scaler in functions taking that.
    """

    kernel: KernelT | None = field(default=None, kw_only=True)
    """
    Base kernel to be used for certain scaling/shifting/resampling operations.
    Must be specified and defaults to catrom
    """

    scaler: ScalerT | None = field(default=None, kw_only=True)
    """Scaler used for scaling operations. Defaults to kernel."""

    shifter: KernelT | None = field(default=None, kw_only=True)
    """Kernel used for shifting operations. Defaults to kernel."""

    def __post_init__(self) -> None:
        self._kernel = Kernel.ensure_obj(self.kernel or Catrom, self.__class__)
        self._scaler = Scaler.ensure_obj(self.scaler or self._kernel, self.__class__)
        self._shifter = Kernel.ensure_obj(
            self.shifter or (self._scaler if isinstance(self._scaler, Kernel) else Catrom), self.__class__
        )

    def __init__(
        self, func: _GeneriScaleNoShift | _GeneriScaleWithShift | F_VD, **kwargs: Any
    ) -> None:
        self.func = func
        self.kwargs = kwargs

    def scale(  # type: ignore
        self, clip: vs.VideoNode, width: int, height: int, shift: tuple[float, float] = (0, 0), **kwargs: Any
    ) -> vs.VideoNode:
        kwargs = self.kwargs | kwargs

        output = None

        if shift != (0, 0):
            try:
                output = self.func(clip, width, height, shift, **kwargs)
            except BaseException:
                try:
                    output = self.func(clip, width=width, height=height, shift=shift, **kwargs)
                except BaseException:
                    pass

        if output is None:
            try:
                output = self.func(clip, width, height, **kwargs)
            except BaseException:
                output = self.func(clip, width=width, height=height, **kwargs)

        return self._finish_scale(output, clip, width, height, shift)

    def _finish_scale(
        self, clip: vs.VideoNode, input_clip: vs.VideoNode, width: int, height: int,
        shift: tuple[float, float] = (0, 0), matrix: MatrixT | None = None,
        copy_props: bool = False
    ) -> vs.VideoNode:
        assert input_clip.format

        if input_clip.format.num_planes == 1:
            clip = plane(clip, 0)

        if (clip.width, clip.height) != (width, height):
            clip = self._scaler.scale(clip, width, height)

        if shift != (0, 0):
            clip = self._shifter.shift(clip, shift)

        assert clip.format

        if clip.format.id != input_clip.format.id:
            clip = self._kernel.resample(clip, input_clip, matrix)

        if copy_props:
            return clip.std.CopyFrameProps(input_clip)

        return clip

    def ensure_scaler(self, scaler: ScalerT) -> Scaler:
        from dataclasses import is_dataclass, replace

        scaler_obj = Scaler.ensure_obj(scaler, self.__class__)

        if is_dataclass(scaler_obj):
            kwargs = dict()

            if hasattr(scaler_obj, 'kernel'):
                kwargs.update(kernel=self.kernel or scaler_obj.kernel)

            if hasattr(scaler_obj, 'scaler'):
                kwargs.update(scaler=self.scaler or scaler_obj.scaler)

            if hasattr(scaler_obj, 'shifter'):
                kwargs.update(shifter=self.shifter or scaler_obj.shifter)

            scaler_obj = replace(scaler_obj, **kwargs)

        return scaler_obj


def scale_var_clip(
    clip: vs.VideoNode,
    width: int | Callable[[Resolution], int] | None, height: int | Callable[[Resolution], int],
    shift: tuple[float, float] | Callable[[Resolution], tuple[float, float]] = (0, 0),
    scaler: Scaler | Callable[[Resolution], Scaler] = Nnedi3(), debug: bool = False
) -> vs.VideoNode:
    """Scale a variable clip to constant or variable resolution."""
    if not debug:
        try:
            return scaler.scale(clip, width, height, shift)  # type: ignore
        except BaseException:
            pass

    _cached_clips = dict[str, vs.VideoNode]()

    no_accepts_var = list[Scaler]()

    def _eval_scale(f: vs.VideoFrame, n: int) -> vs.VideoNode:
        key = f'{f.width}_{f.height}'

        if key not in _cached_clips:
            res = Resolution(f.width, f.height)

            norm_scaler = scaler(res) if callable(scaler) else scaler
            norm_shift = shift(res) if callable(shift) else shift
            norm_height = height(res) if callable(height) else height

            if width is None:
                norm_width = get_w(norm_height, res.width / res.height)
            else:
                norm_width = width(res) if callable(width) else width

            part_scaler = partial(
                norm_scaler.scale, width=norm_width, height=norm_height, shift=norm_shift
            )

            scaled = clip
            if (scaled.width, scaled.height) != (norm_width, norm_height):
                if norm_scaler not in no_accepts_var:
                    try:
                        scaled = part_scaler(clip)
                    except BaseException:
                        no_accepts_var.append(norm_scaler)

                if norm_scaler in no_accepts_var:
                    const_clip = clip.resize.Point(res.width, res.height)

                    scaled = part_scaler(const_clip)

            if debug:
                scaled = scaled.std.SetFrameProps(var_width=res.width, var_height=res.height)

            _cached_clips[key] = scaled

        return _cached_clips[key]

    if callable(width) or callable(height):
        out_clip = clip
    else:
        out_clip = clip.std.BlankClip(width, height)

    return out_clip.std.FrameEval(_eval_scale, clip, clip)


def fdescale_args(
    clip: vs.VideoNode, src_height: float,
    base_height: int | None = None, base_width: int | None = None,
    src_top: float | None = None, src_left: float | None = None,
    src_width: float | None = None, mode: str = 'hw', up_rate: float = 2.0
) -> tuple[KwargsT, KwargsT]:
    base_height = fallback(base_height, mod2(ceil(src_height)))
    base_width = fallback(base_width, get_w(base_height, clip, 2))

    src_width = fallback(src_width, src_height * clip.width / clip.height)

    cropped_width = base_width - 2 * floor((base_width - src_width) / 2)
    cropped_height = base_height - 2 * floor((base_height - src_height) / 2)

    do_h, do_w = 'h' in mode.lower(), 'w' in mode.lower()

    de_args = dict(
        width=cropped_width if do_w else clip.width,
        height=cropped_height if do_h else clip.height
    )

    up_args = dict()

    src_top = fallback(src_top, (cropped_height - src_height) / 2)
    src_left = fallback(src_left, (cropped_width - src_width) / 2)

    if do_h:
        de_args.update(src_height=src_height, src_top=src_top)
        up_args.update(src_height=src_height * up_rate, src_top=src_top * up_rate)

    if do_w:
        de_args.update(src_width=src_width, src_left=src_left)
        up_args.update(src_width=src_width * up_rate, src_left=src_left * up_rate)

    return de_args, up_args
