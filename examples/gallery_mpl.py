"""Native Matplotlib examples for the distribution, limit and matrix presets."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ana_atlas_style import artist_style, matrix_style, use_style


def main():
    use_style("mpl", rc={
        "axes.labelsize": 12, "axes.titlesize": 13, "legend.fontsize": 9,
        "xtick.labelsize": 10, "ytick.labelsize": 10,
    })
    fig, panels = plt.subplots(3, 2, figsize=(10, 10), layout="constrained")
    fig.suptitle("ATLAS style gallery (toy inputs)")
    limit, scan, efficiency, roc, density, correlation = panels.flat

    mass = np.array([300, 400, 500, 600, 700])
    median = np.array([1.5, 1.1, 0.8, 0.9, 1.0])
    limit.fill_between(mass, 0.6 * median, 1.5 * median, label=r"Expected $\pm2\sigma$",
                       **artist_style("expected_2sigma"))
    limit.fill_between(mass, 0.8 * median, 1.2 * median, label=r"Expected $\pm1\sigma$",
                       **artist_style("expected_1sigma"))
    limit.plot(mass, median, label="Expected", **artist_style("expected"))
    limit.plot(mass, [1.4, 1.2, 0.95, 0.8, 1.1], label="Observed",
               **artist_style("data", linestyle="-"))
    limit.set(title="Upper limit", xlabel="Mass [GeV]", ylabel="95% CL upper limit",
              xlim=(285, 715), ylim=(0, 3.1))
    limit.legend(loc="upper right", ncols=2)

    x = np.linspace(-2, 2, 41)
    scan.plot(x, (x - 0.2)**2, label="Observed", **artist_style("series", index=0))
    scan.plot(x, 0.7 * x**2, label="Expected", **artist_style("expected"))
    scan.axhline(1, **artist_style("reference"))
    scan.set(title="Likelihood scan", xlabel=r"$\kappa$", ylabel=r"$-2\Delta\ln L$",
             xlim=(-2, 2), ylim=(0, 5))
    scan.legend(loc="upper center")

    pt = [20, 40, 60, 80, 100]
    efficiency.plot(pt, [0.40, 0.68, 0.83, 0.88, 0.91], label="Simulation",
                    **artist_style("series", index=0))
    efficiency.errorbar(pt, [0.42, 0.67, 0.81, 0.90, 0.92],
                        yerr=[0.05, 0.04, 0.03, 0.02, 0.02], label="Toy data",
                        **artist_style("data"))
    efficiency.set(title="Efficiency", xlabel=r"$p_T$ [GeV]", ylabel="Efficiency",
                   xlim=(15, 105), ylim=(0, 1.05))
    efficiency.legend(loc="lower right")

    tpr = np.linspace(0.15, 1, 30)
    roc.plot(tpr, tpr**3, label="Model A", **artist_style("series", index=0))
    roc.plot(tpr, tpr**5, label="Model B", **artist_style("series", index=1))
    roc.set(title="ROC", xlabel="Signal efficiency", ylabel="Background efficiency",
            xlim=(0, 1), ylim=(1e-4, 1), yscale="log")
    roc.legend(loc="lower right")

    counts = [[21, 8, 1, 0], [4, 43, 12, 2], [0, 11, 54, 17], [0, 1, 13, 38]]
    image = density.imshow(counts, origin="lower", interpolation="nearest",
                           **matrix_style("density", vmin=0))
    density.set(title="Response matrix", xlabel="Truth bin", ylabel="Reco bin",
                xticks=range(4), yticks=range(4))
    fig.colorbar(image, ax=density, label="Events")

    correlations = [[1, 0.62, -0.31, 0.02], [0.62, 1, -0.25, 0.30],
                    [-0.31, -0.25, 1, -0.46], [0.02, 0.30, -0.46, 1]]
    image = correlation.imshow(correlations, origin="lower", interpolation="nearest",
                               **matrix_style("correlation"))
    correlation.set(title="Correlation matrix", xlabel="Parameter", ylabel="Parameter",
                    xticks=range(4), yticks=range(4))
    fig.colorbar(image, ax=correlation, label=r"$\rho$")
    density.minorticks_off()
    correlation.minorticks_off()

    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    fig.savefig(output / "gallery_mpl.pdf")
    fig.savefig(output / "gallery_mpl.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
