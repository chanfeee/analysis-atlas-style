"""Internal Matplotlib defaults; public functions return native, editable values."""

from .colors import COLORS

# Limits, scales, units and panel layout remain with the caller.
MPL_DEFAULTS = {
    "figure.figsize": (8, 6),
    "figure.dpi": 100,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.linewidth": 1.2,
    "axes.grid": False,
    "axes.labelsize": 16,
    "axes.titlesize": 16,
    "axes.labelweight": "normal",
    "font.size": 14,
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "xtick.major.size": 7,
    "ytick.major.size": 7,
    "xtick.minor.size": 3.5,
    "ytick.minor.size": 3.5,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.width": 0.8,
    "ytick.minor.width": 0.8,
    "lines.linewidth": 2,
    "lines.linestyle": "-",
    "lines.marker": "None",
    "lines.markersize": 4.5,
    "lines.markeredgewidth": 1,
    "errorbar.capsize": 0,
    "patch.linewidth": 0.7,
    "hatch.color": COLORS["uncertainty"],
    "hatch.linewidth": 0.55,
    "legend.frameon": False,
    "legend.loc": "best",
    "legend.fontsize": 11.5,
    "legend.columnspacing": 1,
    "legend.handlelength": 1.8,
    "legend.handletextpad": 0.5,
    "legend.borderaxespad": 0.45,
    "legend.labelspacing": 0.4,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.format": "pdf",
    "savefig.dpi": 300,
    "savefig.facecolor": "white",
    "savefig.transparent": False,
}

# Native kwargs only. No coordinates, data or drawing options are hidden here.
ARTIST_DEFAULTS = {
    "data": {
        "color": COLORS["data"], "marker": "o", "linestyle": "none",
        "markersize": 4.5, "linewidth": 1.2,
    },
    "prediction": {
        "color": COLORS["prediction"], "linewidth": 1.5, "linestyle": "-",
    },
    "signal": {
        "color": COLORS["signal"], "linewidth": 2, "linestyle": (0, (6, 2)),
    },
    "alternative": {
        "color": COLORS["alternative"], "linewidth": 2, "linestyle": (0, (3, 2)),
    },
    "background": {"linewidth": 0.7},
    "uncertainty": {
        "facecolor": (1, 1, 1, 0.65), "edgecolor": COLORS["uncertainty"],
        "hatch": "///", "linewidth": 0,
    },
    "reference": {
        "color": COLORS["reference"], "linewidth": 1, "linestyle": "--",
    },
    "annotation": {
        "color": COLORS["annotation"], "fontsize": 11.5,
        "ha": "left", "va": "top",
    },
}

LABEL_DEFAULTS = {"loc": 4, "fontsize": (17, 16, 13.5, 12)}
