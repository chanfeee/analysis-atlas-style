"""ATLAS defaults and optional native artist keyword presets.

Apply the global style before creating figures. Per-call keywords and native
Artist setters remain the last word; no style is reapplied while saving.
"""

from contextlib import contextmanager
from operator import index as integer_index

from ._defaults import ARTIST_DEFAULTS, LABEL_DEFAULTS, MPL_DEFAULTS, SERIES_LINESTYLES
from .colors import BACKGROUND_COLORS, BACKGROUND_FILL_COLORS, MATRIX_COLORS, SERIES_COLORS

__all__ = ["use_atlas_style", "atlas_style", "atlas_label", "artist_style", "matrix_style"]


def artist_style(role, *, index=0, **overrides):
    """Return fresh native kwargs; explicit overrides always win.

    For background fills and comparison curves, index selects a cycling color.
    This function neither draws nor calculates anything. Pass fill=True to
    stairs yourself; histogram baselines and stacking order remain explicit.
    """
    settings = dict(ARTIST_DEFAULTS[role])
    if role in ("background", "series"):
        palette_index = integer_index(index)
        if palette_index < 0:
            raise ValueError(f"{role} index must be non-negative")
    if role == "background":
        color_index = palette_index % len(BACKGROUND_COLORS)
        settings.update(
            facecolor=BACKGROUND_FILL_COLORS[color_index],
            edgecolor=BACKGROUND_COLORS[color_index],
        )
    elif role == "series":
        settings.update(
            color=SERIES_COLORS[palette_index % len(SERIES_COLORS)],
            linestyle=SERIES_LINESTYLES[palette_index % len(SERIES_LINESTYLES)],
        )
    settings.update(overrides)
    return settings


def matrix_style(kind="density", **overrides):
    """Return native imshow or pcolormesh kwargs for a continuous color scale.

    Correlations use a symmetric [-1, 1] range. An explicit norm replaces
    those default limits. Density plots use the caller's value range.
    """
    from matplotlib.colors import LinearSegmentedColormap

    colors = MATRIX_COLORS[kind]
    settings = {"cmap": LinearSegmentedColormap.from_list(f"atlas_{kind}", colors, N=255)}
    if kind == "correlation" and overrides.get("norm") is None:
        settings.update(vmin=-1, vmax=1)
    settings.update(overrides)
    return settings


def _style_settings(*, font, rc):
    import mplhep as hep
    from cycler import cycler
    from matplotlib import font_manager

    # Fail clearly instead of silently substituting a different font family.
    font_manager.findfont(font, fallback_to_default=False)
    settings = dict(hep.style.ATLAS)
    settings.update(MPL_DEFAULTS)
    settings.update(
        {
            "axes.prop_cycle": cycler(color=SERIES_COLORS),
            "font.family": "sans-serif",
            "font.sans-serif": [font],
            "font.monospace": ["DejaVu Sans Mono"],
            "mathtext.fontset": "custom",
            "mathtext.rm": font,
            "mathtext.sf": font,
            "mathtext.it": f"{font}:italic",
            "mathtext.bf": f"{font}:bold",
            "mathtext.bfit": f"{font}:bold:italic",
            "mathtext.tt": "DejaVu Sans Mono",
            "mathtext.cal": f"{font}:italic",
            "mathtext.fallback": "stix",
        }
    )
    settings.update(rc or {})
    return settings


def use_atlas_style(*, font="Arial", rc=None):
    """Apply global defaults; optional native rc overrides are applied last.

    Arial is available on this macOS system. Register another compatible
    TrueType family before passing its name. Call once before creating plots;
    later rc changes, plotting kwargs and Artist setters are left intact.
    """
    import matplotlib as mpl

    mpl.rcParams.update(_style_settings(font=font, rc=rc))


@contextmanager
def atlas_style(*, font="Arial", rc=None):
    """Apply the same defaults temporarily, restoring the surrounding rc state."""
    import matplotlib as mpl

    with mpl.rc_context(rc=_style_settings(font=font, rc=rc)):
        yield


def atlas_label(ax, *, text, data, com, lumi=None, **kwargs):
    """Add an ATLAS label; com is in TeV and lumi in inverse femtobarns.

    Use text="" for the plain publication label. Set data=False for a
    simulation label. Status and dataset information are always explicit.
    Additional keywords override LABEL_DEFAULTS and go to mplhep.atlas.label.
    """
    import matplotlib as mpl
    import mplhep as hep

    settings = dict(LABEL_DEFAULTS)
    settings["fontname"] = mpl.rcParams["font.sans-serif"][0]
    settings.update(kwargs)
    return hep.atlas.label(text, ax=ax, data=data, com=com, lumi=lumi, **settings)
