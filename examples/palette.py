"""Render role defaults and the series cycle: python -m plotting.examples.palette."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from plotting import SERIES_COLORS, SERIES_FILL_COLORS, use_atlas_style


def main():
    use_atlas_style()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.1))
    names = ("Blue", "Violet", "Teal", "Gray", "Orange")
    groups = (
        ("Line / marker accents", list(zip(names, SERIES_COLORS))),
        ("Stacked-area fills", list(zip(names, SERIES_FILL_COLORS))),
    )
    for ax, (title, entries) in zip(axes, groups):
        ax.set(xlim=(0, 1), ylim=(0, 6))
        ax.axis("off")
        ax.text(0, 5.65, title, fontsize=17, fontweight="bold")
        for row, (name, color) in enumerate(entries):
            y = 4.9 - row * 0.85
            ax.add_patch(Rectangle((0, y - 0.2), 0.16, 0.4, facecolor=color))
            ax.text(0.21, y, name, va="center", fontsize=13)
            ax.text(0.71, y, color, va="center", fontsize=12, family="monospace")
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.12, top=0.96, wspace=0.18)
    fig.text(
        0.06, 0.045,
        "Distribution colors based on ATLAS PRL 132, 221801 (Fig. 2).",
        fontsize=10,
    )
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "palette.pdf")
    fig.savefig(output / "palette.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
