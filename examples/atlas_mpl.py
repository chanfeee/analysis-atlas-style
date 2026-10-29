"""Run from the project root: python -m plotting.examples.atlas_mpl."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plotting import artist_style, atlas_label, use_atlas_style


def main():
    use_atlas_style()
    edges = np.arange(60, 170, 10)
    sample = np.array([10, 26, 70, 125, 92, 53, 26, 14, 8, 3])
    expected = np.array([12, 25, 65, 115, 100, 50, 28, 16, 7, 4])
    signal = np.array([0, 0, 1, 5, 12, 22, 12, 5, 1, 0])

    fig, ax = plt.subplots()
    # This 10% band is illustrative toy input, not an uncertainty prescription.
    band = ax.fill_between(
        edges,
        np.r_[0.9 * expected, 0.9 * expected[-1]],
        np.r_[1.1 * expected, 1.1 * expected[-1]],
        step="post",
        label="Toy uncertainty",
        **artist_style("uncertainty"),
    )
    prediction = ax.stairs(
        expected, edges, label="Toy prediction", **artist_style("prediction"),
    )
    signal_line = ax.stairs(
        signal, edges, label="Toy signal", **artist_style("signal"),
    )
    points = ax.errorbar(
        (edges[:-1] + edges[1:]) / 2,
        sample,
        yerr=np.sqrt(sample),
        label="Toy sample",
        **artist_style("data"),
    )
    ax.set(
        xlabel=r"$m$ [GeV]",
        ylabel="Events / 10 GeV",
        xlim=(60, 160),
        ylim=(0, 190),
    )
    atlas_label(ax, text="", data=False, com=13)
    ax.legend(handles=[points, prediction, band, signal_line], loc="upper right")

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "atlas_mpl.pdf")
    fig.savefig(output / "atlas_mpl.png", dpi=150)
    plt.close(fig)
    print(f"Saved ATLAS style examples to {output}")


if __name__ == "__main__":
    main()
