"""Journal-inspired color defaults, mirrored in root/AtlasColors.h.

Accents use the first five ggsci NEJM colors, reordered by role. Area fills
mix 45% accent with 55% white; they are opaque so stacked layers do not mix.
These are project choices, not official journal or ATLAS color requirements.
Source: https://nanx.me/ggsci/reference/pal_nejm.html
"""

SERIES_COLORS = (
    "#0072B5",  # blue
    "#BC3C29",  # red
    "#20854E",  # green
    "#E18727",  # orange
    "#7876B1",  # violet
)


def _light_fill(color):
    channels = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{round(0.45 * c + 0.55 * 255):02X}" for c in channels)


SERIES_FILL_COLORS = tuple(_light_fill(color) for color in SERIES_COLORS)

COLORS = {
    "data": "#000000",
    "prediction": "#303030",
    "signal": SERIES_COLORS[1],
    "background": SERIES_COLORS[0],
    "alternative": SERIES_COLORS[4],
    "uncertainty": "#999999",
    "reference": "#404040",
    "annotation": "#444444",
}

FILL_COLORS = {
    "prediction": _light_fill(COLORS["prediction"]),
    "signal": SERIES_FILL_COLORS[1],
    "background": SERIES_FILL_COLORS[0],
    "alternative": SERIES_FILL_COLORS[4],
}
