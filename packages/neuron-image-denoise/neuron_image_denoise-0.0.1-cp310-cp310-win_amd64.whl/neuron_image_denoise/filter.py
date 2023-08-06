import numpy as np
from . import _filter


def adaptive_denoise(img: np.ndarray, ada_interval=(2, 3, 3), flare_interval=(2, 8, 8),
                     ada_sampling=3, flare_sampling=8, flare_weight=.02, atten_depth=4., flare_x=True, flare_y=True):
    """
    Remove background noise and flare.

    :param img: 3D neuron fluorescent image array, 16bit.
    :param ada_interval: stride for adaptive threshold.
    :param flare_interval: stride for removing flare effect.
    :param ada_sampling: number of steps for adaptive threshold.
    :param flare_sampling: number of steps for removing flare effect.
    :param flare_weight: the weight of flare reduction.
    :param atten_depth: the unit attenuation distance of the flare.
    :param flare_x: whether calculate flare along x, when both do, take bigger.
    :param flare_y: whether calculate flare along y, when both do, take bigger.
    :return: denoised 3D image array, 16bit.
    """
    return _filter.adaptive_denoise(img, ada_interval, flare_interval, ada_sampling, flare_sampling, flare_weight, atten_depth,
                                    flare_x, flare_y)


def adaptive_denoise_16to8(img: np.ndarray, lower: int | float = 0, upper: int | float = 255, **kwargs):
    """
    The adaptive denoising is designed for 16bit raw image with full details.
    This wrapper appends a bit conversion afterward, by clipping and linear scaling.

    keyword arguments are passed to `adaptive_denoise`

    :param img: 3D neuron fluorescent image array, 16bit.
    :param lower: the lower threshold or quantile.
    :param upper: the lower threshold or quantile.
    :return: denoised 3D image array, 8bit.
    """
    assert img.dtype == np.uint16
    assert img.ndim == 3
    img = adaptive_denoise(img, **kwargs)
    if type(lower) is float:
        lower = np.quantile(img, lower)
    if type(upper) is float:
        upper = np.quantile(img, upper)
    return ((img.clip(lower, upper) - lower) / (upper - lower) * 255).astype(np.uint8)