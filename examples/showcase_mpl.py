"""Full ATLAS style example: python -m ana_atlas_style.examples.showcase_mpl.

All layout and histogram operations stay in this editable example. Both
backends read showcase_inputs.dat. These are toy inputs, not ATLAS results.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

from ana_atlas_style import artist_style, atlas_label, use_atlas_style


def make_figure():
    use_atlas_style()
    inputs = Path(__file__).with_name("showcase_inputs.dat")
    low, high, a, b, c, signal, sample, uncertainty, alternative = np.loadtxt(
        inputs, unpack=True
    )
    edges = np.r_[low, high[-1]]
    centers = (low + high) / 2
    nominal = a + b + c
    statistical = np.sqrt(sample)

    # Native GridSpec: the caller owns both axes and all layout decisions.
    fig = plt.figure(figsize=(8.8, 7.8))
    grid = fig.add_gridspec(
        2, 1, height_ratios=(3.4, 1), hspace=0.05,
        left=0.14, right=0.97, bottom=0.12, top=0.95,
    )
    ax = fig.add_subplot(grid[0])
    ratio_ax = fig.add_subplot(grid[1], sharex=ax)

    # Large areas use pale opaque fills; curves and edges retain full accents.
    background_c = ax.stairs(
        c, edges, baseline=0, fill=True,
        label="Background C", **artist_style("background", index=2),
    )
    background_b = ax.stairs(
        b + c, edges, baseline=c, fill=True,
        label="Background B", **artist_style("background", index=1),
    )
    background_a = ax.stairs(
        nominal, edges, baseline=b + c, fill=True,
        label="Background A", **artist_style("background", index=0),
    )

    band = ax.fill_between(
        edges,
        np.r_[nominal - uncertainty, (nominal - uncertainty)[-1]],
        np.r_[nominal + uncertainty, (nominal + uncertainty)[-1]],
        step="post", label="Total unc.", **artist_style("uncertainty"),
    )
    ratio_ax.fill_between(
        edges,
        np.r_[1 - uncertainty / nominal, 1 - uncertainty[-1] / nominal[-1]],
        np.r_[1 + uncertainty / nominal, 1 + uncertainty[-1] / nominal[-1]],
        step="post", **artist_style("uncertainty"),
    )

    prediction = ax.stairs(
        nominal, edges, label="Total pred.", **artist_style("prediction"),
    )
    alternative_line = ax.stairs(
        alternative, edges, label="Alt. model", **artist_style("alternative"),
    )
    signal_line = ax.stairs(
        4 * signal, edges, label=r"Signal $\times 4$", **artist_style("signal"),
    )
    points = ax.errorbar(
        centers, sample, yerr=statistical, label="Toy sample", **artist_style("data"),
    )

    ax.set_yscale("log")
    ax.set(xlim=(60, 220), ylim=(0.6, 60000))
    ax.set_ylabel("Events / 10 GeV")
    ax.tick_params(axis="x", which="both", labelbottom=False)
    atlas_label(
        ax, text="", data=False, com=13, lumi=140,
    )
    ax.text(
        0.04, 0.79, "Toy inputs - illustrative region", transform=ax.transAxes,
        **artist_style("annotation"),
    )
    ax.legend(
        handles=[points, prediction, alternative_line, signal_line,
                 background_a, background_b, background_c, band],
        loc="upper right", ncols=2,
    )

    # Numerator statistics only; denominator uncertainty is a separate band.
    ratio_ax.axhline(1, **artist_style("reference"))
    ratio_ax.stairs(
        alternative / nominal, edges,
        **artist_style("alternative", linewidth=1.8),  # Local override.
    )
    ratio_ax.errorbar(
        centers, sample / nominal, yerr=statistical / nominal,
        **artist_style("data"),
    )
    ratio_ax.set_ylim(0.65, 1.35)
    ratio_ax.set_xlabel(r"$m$ [GeV]", fontsize=17)
    ratio_ax.set_ylabel("Toy / Pred.", fontsize=13, loc="center", labelpad=14)
    ratio_ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ratio_ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    ratio_ax.xaxis.set_major_locator(MultipleLocator(20))
    ratio_ax.xaxis.set_minor_locator(MultipleLocator(5))
    return fig, (ax, ratio_ax)


def main():
    fig, _ = make_figure()
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "showcase_mpl.pdf")
    fig.savefig(output / "showcase_mpl.png", dpi=160)
    plt.close(fig)
    print(f"Saved comprehensive Matplotlib example to {output}")


if __name__ == "__main__":
    main()
