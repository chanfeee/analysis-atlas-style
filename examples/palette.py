"""Render role defaults and the series cycle: python -m ana_atlas_style.examples.palette."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from ana_atlas_style import BACKGROUND_COLORS, BACKGROUND_FILL_COLORS, SERIES_COLORS, use_style


def main():
    use_style("mpl")
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.8))
    groups = (
        ("Line / marker accents",
         zip(("Blue", "Violet", "Teal", "Gray", "Orange"), SERIES_COLORS, SERIES_COLORS)),
        ("MC stack fills",
         zip(("Navy", "Slate blue", "Pale blue", "Wine red",
              "Sage", "Muted gold", "Lilac", "Warm ivory"),
             BACKGROUND_FILL_COLORS, BACKGROUND_COLORS)),
    )
    for ax, (title, entries) in zip(axes, groups):
        ax.set(xlim=(0, 1), ylim=(0, 8.5))
        ax.axis("off")
        ax.text(0, 8.15, title, fontsize=17, fontweight="bold")
        for row, (name, color, edge) in enumerate(entries):
            y = 7.45 - row * 0.96
            ax.add_patch(Rectangle((0, y - 0.2), 0.16, 0.4, facecolor=color, edgecolor=edge))
            ax.text(0.21, y, name, va="center", fontsize=13)
            ax.text(0.71, y, color, va="center", fontsize=12, family="monospace")
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.12, top=0.96, wspace=0.18)
    fig.text(
        0.06, 0.045,
        "MC stack fills have their own palette. Curve accents draw on ATLAS PRL 132, 221801 (Fig. 2).",
        fontsize=10,
    )
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "palette.pdf")
    fig.savefig(output / "palette.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
