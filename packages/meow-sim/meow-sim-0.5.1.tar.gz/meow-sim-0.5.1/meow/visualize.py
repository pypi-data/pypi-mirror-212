""" Visualizations for common meow-datatypes """

from typing import Any

import numpy as np

try:
    import matplotlib.pyplot as plt  # fmt: skip


except ImportError:
    plt = None

try:
    import gdsfactory as gf  # fmt: skip
except ImportError:
    gf = None

try:
    from jaxlib.xla_extension import DeviceArray  # fmt: skip # type: ignore
except ImportError:
    DeviceArray = None


def _visualize_s_matrix(S, fmt=None, title=None, show=True, phase=False, ax=None):
    import matplotlib.pyplot as plt  # fmt: skip
    if phase:
        fmt = ".0f"
    else:
        fmt = ".3f"

    Z = np.abs(S)
    y, x = np.arange(Z.shape[0])[::-1], np.arange(Z.shape[1])
    Y, X = np.meshgrid(y, x)

    if ax:
        plt.sca(ax)
    else:
        plt.figure(figsize=(2 * x.shape[0] / 3, 2 * y.shape[0] / 3))

    plt.pcolormesh(X, Y, Z[::-1].T, cmap="Greys", vmin=0.0, vmax=2.0 * Z.max())

    coords_ = np.concatenate(
        [np.array([x[0] - 1]), x, np.array([x[-1] + 1])], axis=0, dtype=float
    )
    labels = ["" for _ in coords_]
    plt.xticks(coords_ + 0.5, labels)
    plt.xlim(coords_[0] + 0.5, coords_[-1] - 0.5)

    coords_ = np.concatenate(
        [np.array([y[0] + 1]), y, np.array([y[-1] - 1])], axis=0, dtype=float
    )
    coords_ = coords_[::-1]  # reverse
    labels = ["" for _ in coords_]
    plt.yticks(coords_ + 0.5, labels)
    plt.ylim(coords_[-1] - 0.5, coords_[0] + 0.5)
    plt.grid(True)

    for x, y, z in zip(X.ravel(), Y.ravel(), S[::-1].T.ravel()):
        if np.abs(z) > 0.0005:
            if phase:
                z = np.angle(z) * 180 / np.pi
            text = eval(f"f'{{z:{fmt}}}'")  # 😅
            text = text.replace("+", "\n+")
            text = text.replace("-", "\n-")
            if text[0] == "\n":
                text = text[1:]
            plt.text(x, y, text, ha="center", va="center", fontsize=8)

    if title is not None:
        plt.title(title)

    if show:
        plt.show()


def _visualize_s_pm_matrix(Spm, fmt=None, title=None, show=True, ax=None):
    import matplotlib.pyplot as plt  # fmt: skip

    S, pm = Spm
    _visualize_s_matrix(S, fmt=fmt, title=title, show=False, ax=ax)
    num_left = len([p for p in pm if "left" in p])
    Z = np.abs(S)
    _, x = np.arange(Z.shape[0])[::-1], np.arange(Z.shape[1])

    plt.axvline(x[num_left] - 0.5, color="red")
    plt.axhline(x[num_left] - 0.5, color="red")

    if show:
        plt.show()


def _visualize_overlap_density(
    two_modes,
    conjugated=True,
    x_symmetry=False,
    y_symmetry=False,
    ax=None,
    n_cmap=None,
    mode_cmap=None,
    num_levels=8,
    show=True,
):
    import matplotlib.pyplot as plt  # fmt: skip

    from .mode import Mode  # fmt: skip

    mode1, mode2 = two_modes
    if conjugated:
        cross = mode1.Ex * mode2.Hy.conj() - mode1.Ey * mode2.Hx.conj()
    else:
        cross = mode1.Ex * mode2.Hy - mode1.Ey * mode2.Hx
    if x_symmetry:
        cross = 0.5 * (cross + cross[::-1])
    if y_symmetry:
        cross = 0.5 * (cross + cross[:, ::-1])
    zeros = np.zeros_like(cross)
    overlap = Mode(
        neff=mode1.neff,
        cs=mode1.cs,
        Ex=cross,
        Ey=zeros,
        Ez=zeros,
        Hx=zeros,
        Hy=zeros,
        Hz=zeros,
    )
    if ax is None:
        W, H = _figsize_visualize_mode(mode1.cs, 5)
        _, ax = plt.subplots(1, 3, figsize=(3 * W, H))

    field = "Ex" if mode1.te_fraction > 0.5 else "Hx"
    mode1._visualize(
        title=f"mode 1: {field}",
        fields=[field],
        ax=ax[0],
        n_cmap=n_cmap,
        mode_cmap=mode_cmap,
        num_levels=num_levels,
        show=False,
    )

    field = "Ex" if mode2.te_fraction > 0.5 else "Hx"
    mode2._visualize(
        title=f"mode 2: {field}",
        fields=[field],
        ax=ax[1],
        n_cmap=n_cmap,
        mode_cmap=mode_cmap,
        num_levels=num_levels,
        show=False,
    )

    title = "overlap density" + ("" if conjugated else " (no conjugations)")
    p = overlap._visualize(
        title=title,
        fields=["Ex"],
        ax=ax[2],
        n_cmap=n_cmap,
        mode_cmap=mode_cmap,
        num_levels=num_levels,
        show=False,
    )

    if show:
        plt.show()

    return p


def _visualize_gdsfactory(comp):
    import gdsfactory as gf  # fmt: skip

    gf.plot(comp)  # type: ignore


def _is_s_matrix(obj: Any):
    return (
        (
            isinstance(obj, np.ndarray)
            or (DeviceArray is not None and isinstance(obj, DeviceArray))
        )
        and obj.ndim == 2
        and obj.shape[0] > 1
        and obj.shape[1] > 1
    )


def _is_two_tuple(obj):
    try:
        x, y = obj
        return True
    except Exception:
        return False


def _figsize_visualize_mode(cs, W0):
    x_min, x_max = cs.mesh.x.min(), cs.mesh.x.max()
    y_min, y_max = cs.mesh.y.min(), cs.mesh.y.max()
    delta_x = x_max - x_min
    delta_y = y_max - y_min
    aspect = delta_y / delta_x
    W0 = 6.4
    W, H = W0 + 1, W0 * aspect + 1
    return W, H


def _visualize_modes(
    modes,
    n_cmap=None,
    mode_cmap=None,
    num_levels=8,
    operation=lambda x: np.abs(x) ** 2,
    show=True,
):
    import matplotlib.pyplot as plt  # fmt: skip
    from matplotlib.colors import LinearSegmentedColormap  # fmt: skip
    from mpl_toolkits.axes_grid1 import make_axes_locatable  # fmt: skip

    num_modes = len(modes)
    cs = modes[0].cs
    X, Y, n = cs.mesh.Xz, cs.mesh.Yz, cs.nz
    W, H = _figsize_visualize_mode(cs, 6.4)

    n_cmap = LinearSegmentedColormap.from_list(
        name="c_cmap", colors=["#ffffff", "#c1d9ed"]
    )
    fig, ax = plt.subplots(
        num_modes,
        2,
        figsize=(2 * W, num_modes * H),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for i, m in enumerate(modes):
        m._visualize(
            title=None,
            fields=["Ex", "Hx"],
            ax=ax[i],
            n_cmap=n_cmap,
            mode_cmap=mode_cmap,
            num_levels=num_levels,
            operation=operation,
            show=False,
        )
    fig.subplots_adjust(hspace=0, wspace=2 / (2 * W))
    if show:
        plt.show()


def visualize(obj: Any, **kwargs: Any):
    """visualize any meow object

    Args:
        obj: the meow object to visualize
        **kwargs: extra configuration to visualize the object

    Note:
        Most meow objects have a `._visualize` method.
        Check out its help to see which kwargs are accepted.
    """
    from .base_model import BaseModel  # fmt: skip
    from .mode import Mode  # fmt: skip
    from .structures import Structure, visualize_structures  # fmt: skip

    # if isinstance(obj, Mode):
    #    return _visualize_mode(obj)
    if plt is None:
        return obj

    if isinstance(obj, list) and all(isinstance(o, Mode) for o in obj):
        return _visualize_modes(obj)
    elif isinstance(obj, BaseModel):
        return obj._visualize(**kwargs)
    elif _is_two_tuple(obj) and all(isinstance(o, Mode) for o in obj):
        return _visualize_overlap_density(obj, **kwargs)
    elif _is_s_matrix(obj):
        _visualize_s_matrix(obj, **kwargs)
    elif _is_two_tuple(obj) and _is_s_matrix(obj[0]) and isinstance(obj[1], dict):
        _visualize_s_pm_matrix(obj, **kwargs)
    elif gf is not None and isinstance(obj, gf.Component):
        _visualize_gdsfactory(obj, **kwargs)
    else:
        try:
            (*objs,) = obj  # type: ignore
        except TypeError:
            return obj

        if all(isinstance(obj, Structure) for obj in objs):
            return visualize_structures(objs, **kwargs)
        return objs


vis = visualize  # shorthand for visualize
