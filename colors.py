"""ATLAS PRL color defaults, mirrored in root/AtlasColors.h.

Signal and comparison accents draw on PRL 132, 221801, Fig. 2.
Expected-limit bands follow PRL 133, 101801, Fig. 2.
"""

SERIES_COLORS = (
    "#4292C6",  # blue
    "#6A51A3",  # violet
    "#278471",  # teal edge
    "#666666",  # gray
    "#FF7700",  # orange
)

SERIES_FILL_COLORS = (
    "#BCE1FF",  # QCD track
    "#BCB1D6",  # violet mixed with white
    "#48C9B0",  # W+jets
    "#D6D6D6",  # other backgrounds
    "#FFC28C",  # orange mixed with white
)

BACKGROUND_COLORS = (
    "#33395B", "#5D74A2", "#C4D8F2", "#8E2D30",
    "#82AD92", "#CFAB66", "#AB99C6", "#F2E8E3",
)
BACKGROUND_FILL_COLORS = BACKGROUND_COLORS

COLORS = {
    "data": "#000000",
    "prediction": "#333333",
    "signal": SERIES_COLORS[1],
    "background": BACKGROUND_COLORS[0],
    "alternative": SERIES_COLORS[4],
    "uncertainty": "#666666",
    "reference": "#404040",
    "annotation": "#444444",
}

LIMIT_BAND_COLORS = {
    "expected_1sigma": "#4AD9D9",
    "expected_2sigma": "#FDC536",
}

FILL_COLORS = {
    "prediction": SERIES_FILL_COLORS[3],
    "signal": SERIES_FILL_COLORS[1],
    "background": BACKGROUND_FILL_COLORS[0],
    "alternative": SERIES_FILL_COLORS[4],
}

MATRIX_COLORS = {
    "density": ("#FFFFFF", SERIES_FILL_COLORS[0], SERIES_COLORS[0], "#174568"),
    "correlation": ("#2166AC", "#FFFFFF", "#C62F3B"),
}
