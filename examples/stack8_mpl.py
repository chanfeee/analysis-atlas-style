"""Show all eight MC colors on a native Matplotlib stack with toy inputs."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

from ana_atlas_style import artist_style, atlas_label, use_style


def main():
    use_style("mpl")
    bins = np.loadtxt(Path(__file__).with_name("stack8_inputs.dat"))
    edges = np.r_[bins[:, 0], bins[-1, 1]]
    centers = (edges[:-1] + edges[1:]) / 2
    labels = (
        r"$t\bar{t}$", r"$W$+jets", r"$Z$+jets", "Single top", "Diboson",
        r"$t\bar{t}+V$", "Multijet", "Other",
    )
    components = bins[:, 2:10].T
    nominal = components.sum(axis=0)
    observed, signal, relative_unc, alternate_ratio = bins[:, 10:].T

    fig, (ax, ratio) = plt.subplots(
        2, 1, figsize=(8.8, 7.8), sharex=True,
        gridspec_kw={"height_ratios": (3.4, 1), "hspace": 0.05,
                     "left": 0.14, "right": 0.97, "bottom": 0.12, "top": 0.95},
    )
    baseline = np.zeros_like(nominal)
    layers = []
    for index in reversed(range(len(labels))):
        top = baseline + components[index]
        layer = ax.stairs(top, edges, baseline=baseline, fill=True,
                          label=labels[index],
                          **artist_style("background", index=index))
        layers.append(layer)
        baseline = top

    low, high = nominal * (1 - relative_unc), nominal * (1 + relative_unc)
    band = ax.fill_between(
        edges, np.r_[low, low[-1]], np.r_[high, high[-1]],
        step="post", label="Total unc.", **artist_style("uncertainty"),
    )
    prediction = ax.stairs(nominal, edges, baseline=None, label="Total pred.",
                           **artist_style("prediction"))
    alternate = ax.stairs(nominal * alternate_ratio, edges, baseline=None,
                          label="Alt. model", **artist_style("alternative"))
    signal_line = ax.stairs(signal, edges, baseline=None, label="Toy signal",
                            **artist_style("signal"))
    data = ax.errorbar(centers, observed, yerr=np.sqrt(observed), label="Pseudo-data",
                       **artist_style("data"))
    ax.set(ylabel="Events / 10 GeV", yscale="log", ylim=(6, 32000),
           xlim=(edges[0], edges[-1]))
    atlas_label(ax, text="", data=False, com=13, lumi=140)
    ax.text(0.04, 0.78, "Toy validation region", transform=ax.transAxes,
            **artist_style("annotation"))
    ax.legend(handles=[data, prediction, alternate, signal_line, band, *reversed(layers)],
              ncols=2, loc="upper right", fontsize=10.5)

    ratio.fill_between(
        edges, np.r_[1 - relative_unc, 1 - relative_unc[-1]],
        np.r_[1 + relative_unc, 1 + relative_unc[-1]],
        step="post", **artist_style("uncertainty"),
    )
    ratio.axhline(1, **artist_style("reference"))
    ratio.stairs(alternate_ratio, edges, baseline=None,
                 **artist_style("alternative", linewidth=1.6))
    ratio.errorbar(centers, observed / nominal, yerr=np.sqrt(observed) / nominal,
                   **artist_style("data"))
    ratio.set(xlabel=r"$m_{jj}$ [GeV]", ylim=(0.7, 1.3))
    ratio.set_ylabel("Data / Pred.", fontsize=12, loc="center")
    ratio.yaxis.set_major_locator(MultipleLocator(0.2))
    ratio.yaxis.set_minor_locator(MultipleLocator(0.1))
    ratio.xaxis.set_major_locator(MultipleLocator(20))
    ratio.xaxis.set_minor_locator(MultipleLocator(5))

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "stack8_mpl.pdf")
    fig.savefig(output / "stack8_mpl.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
