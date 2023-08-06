from typing import Callable, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats


def list_all_feature_names() -> List[str]:
    """
    Returns a list of available feature names.
    """
    return list(name_dict.keys())


def get_freq_amp(x: np.ndarray, fs: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Examples
    --------
    >>> n_secs = 5
    >>> fs = 256
    >>> true_freqs = np.array([11, 23, 31, 41])
    >>> true_amps = np.array([13, 29, 37, 43])
    >>> t = np.linspace(0, n_secs, n_secs * fs, endpoint=False)
    >>> x = (np.sin(2 * np.pi * t[..., np.newaxis] * true_freqs) * true_amps).sum(1)
    >>> freq, amps = get_freq_amp(x=x, fs=fs)
    """
    if np.ndim(x) == 1:
        x = x.reshape(1, -1)
    n = x.shape[-1]
    freq = sp.fft.fftfreq(n, d=1 / fs)
    fhat = sp.fft.fft(x)
    amp = 2 * np.abs(fhat) / n
    amp[..., 0] = 0
    return freq[: n // 2].copy(), amp[..., : n // 2].copy()


def get_ratio_max_upper_fence(x: np.ndarray, axis=-1, keepdims=False) -> np.ndarray:
    """
    Examples
    --------
    >>> feat = get_ratio_max_upper_fence(np.random.randn(10, 1024))
    >>> feat.shape
    (10,)
    >>> feat = get_ratio_max_upper_fence(np.random.randn(10, 1024), keepdims=True)
    >>> feat.shape
    (10, 1)
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]
    _max = np.max(x, axis=axis, keepdims=keepdims)
    _upper_fence = get_upper_fence(x, axis=axis, keepdims=keepdims)
    return _max / _upper_fence


def get_rmeds(x: np.ndarray, axis=-1, keepdims=False) -> np.ndarray:
    """
    Examples
    --------
    >>> rmeds = get_rmeds(np.random.randn(10, 1024))
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]
    return np.sqrt(np.median(x**2, axis=axis, keepdims=keepdims))


def get_rms(x: np.ndarray, axis=-1, keepdims=False) -> np.ndarray:
    """
    Examples
    --------
    >>> rms = get_rms(np.random.randn(10, 1024))
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]
    return np.sqrt(np.mean(x**2, axis=axis, keepdims=keepdims))


def get_upper_fence(x: np.ndarray, axis=-1, keepdims=False) -> np.ndarray:
    """
    Examples
    --------
    >>> upper_fence = get_upper_fence(np.random.randn(3, 1024))
    >>> upper_fence.shape
    (3,)
    >>> upper_fence = get_upper_fence(np.random.randn(3, 1024), keepdims=True)
    >>> upper_fence.shape
    (3, 1)
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]

    _q3 = np.quantile(x, axis=axis, q=0.75, keepdims=keepdims)
    _iqr = stats.iqr(x, axis=axis, keepdims=keepdims)
    return _q3 + 1.5 * _iqr


def get_zcr(x: np.ndarray, axis=-1, keepdims=False) -> np.ndarray:
    """
    Examples
    --------
    >>> zcr = get_zcr(np.random.randn(10, 1024))
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]
    zc = np.abs(np.diff(np.sign(x), axis=axis)).sum(axis, keepdims=keepdims) / 2
    return zc / x.shape[1]


name_dict: Dict[str, Callable[..., np.ndarray]] = {
    "entropy": stats.entropy,
    "kurtosis": stats.kurtosis,
    "mad": stats.median_abs_deviation,
    "max": np.max,
    "mean": np.mean,
    "median": np.median,
    "ratio_max_upper_fence": get_ratio_max_upper_fence,
    "rmeds": get_rmeds,
    "rms": get_rms,
    "skew": stats.skew,
    "std": np.std,
    "upper_fence": get_upper_fence,
    "zcr": get_zcr,
}


def get_feature(
    x: np.ndarray,
    names: Union[str, List[str], None] = None,
) -> pd.DataFrame:
    """
    Examples
    --------
    >>> n_samples = 4
    >>> n_size = 1024
    >>> x = np.random.randn(n_samples, n_size)
    >>> feats = get_feature(x)
    >>> isinstance(feats, pd.DataFrame)
    True
    >>> feats = get_feature(x, names="entropy")
    >>> feats.shape
    (4, 1)
    >>> feats = get_feature(x, names=["entropy", "kurtosis"])
    >>> feats.shape
    (4, 2)
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]

    if names is None:
        names = list_all_feature_names()

    if not isinstance(names, list):
        names = [names]

    if not set(names).issubset(names):
        raise TypeError("Unsupported provided name.")

    feats = []
    for name in names:
        func = name_dict[name]
        _x = abs(x.copy()) if name == "entropy" else x.copy()
        partial_feats = func(_x, axis=1)
        feats.append(partial_feats)

    feats = np.array(feats).T.reshape(x.shape[0], len(names))
    feats = pd.DataFrame(feats, columns=names)

    return feats


def get_spectral_feature(
    x: np.ndarray,
    *,
    fs: int,
    freq_intervals: Optional[List[List[int]]] = None,
    names: Union[str, List[str], None] = None,
    major_freq: Union[int, None] = None,
    ratio_major_orders: Optional[List[List[int]]] = None,
    eps: Union[int, None] = None,
) -> pd.DataFrame:
    """
    Get features from spectra.

    Examples
    --------
    >>> n_samples = 10
    >>> fs = 1024
    >>> x = np.random.randn(n_samples, fs)
    >>> features = get_spectral_feature(x=x, fs=fs)
    >>> features = get_spectral_feature(x=x, fs=fs, freq_intervals=[[50, 70]])
    >>> isinstance(features, pd.DataFrame)
    True
    >>> features = get_spectral_feature(x=x, fs=fs, freq_intervals=[[50, 70]], names="entropy")
    >>> features.shape
    (10, 1)
    >>> features = get_spectral_feature(x=x, fs=fs, freq_intervals=[[50, 70], [110, 130]], names=["kurtosis"])
    >>> features.shape
    (10, 2)
    >>> features = get_spectral_feature(
    ... x=x,
    ... fs=fs,
    ... freq_intervals=[[50, 70], [110, 130]],
    ... names=["entropy", "kurtosis"],
    ... )
    >>> features.shape
    (10, 4)
    >>> features.columns
    Index(['entropy_50_70', 'entropy_110_130', 'kurtosis_50_70',
           'kurtosis_110_130'],
          dtype='object')
    >>> features = get_spectral_feature(x=x, fs=fs, major_freq=60, ratio_major_orders=[[1, 3], [2, 3]], eps=10)
    """
    x = x.copy()
    if np.ndim(x) == 1:
        x = x[np.newaxis, ...]

    if names is None:
        names = list_all_feature_names()

    if not isinstance(names, list):
        names = [names]

    if not set(names).issubset(names):
        raise TypeError("Unsupported provided name.")

    if freq_intervals is None:
        freq_intervals = [[0, fs // 2]]

    new_column_to_dict = {}
    if major_freq is not None:
        if ratio_major_orders is None:
            raise ValueError("The argument ratio_major_orders should not be None.")

        if eps is None:
            raise ValueError("The argument eps should be of integer or of float type.")

        if "max" not in names:
            names.append("max")

        seen: Set[int] = set()
        for interval in ratio_major_orders:
            for order in interval:
                if order not in seen:
                    seen.add(order)
                    left = order * major_freq - eps
                    right = order * major_freq + eps
                    freq_intervals.append([left, right])
                    new_column_to_dict[f"max_{left}_{right}"] = f"max_{order}x"

    freq, amps = get_freq_amp(x=x, fs=fs)

    feats = []
    for name in names:
        feats_given_name = []
        for interval in freq_intervals:
            start = interval[0]
            end = interval[-1]
            cond = np.where((start < freq) & (freq < end))[0]

            partial_feats = get_feature(x=amps[..., cond], names=name)
            feats_given_name.append(partial_feats.values.ravel())
        feats_given_name = np.array(feats_given_name).T
        feats.append(feats_given_name)
    feats = np.concatenate(feats, axis=1)

    columns = [f"{n}_{seg[0]}_{seg[1]}" for n in names for seg in freq_intervals]
    feats = pd.DataFrame(feats, columns=columns)
    feats = feats.rename(columns=new_column_to_dict)

    if major_freq is not None and ratio_major_orders is not None and eps is not None:
        for order in ratio_major_orders:
            o1, o2 = order
            col1 = f"max_{o1}x"
            col2 = f"max_{o2}x"
            ratio_col = f"ratio_order_{o1}x_{o2}x"

            feats[ratio_col] = feats[col1] / feats[col2]
            columns.append(ratio_col)

    assert feats.shape == (x.shape[0], len(columns))

    return feats
