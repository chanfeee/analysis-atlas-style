"""ROOT gallery using native graphs, histograms, and pads with toy inputs."""

from array import array
from pathlib import Path

import ROOT

from plotting import use_root_style


def main():
    ROOT.gROOT.SetBatch(True)
    use_root_style()
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)

    canvas = ROOT.TCanvas("gallery", "", 1100, 850)
    canvas.Divide(2, 2)
    objects = []  # Keep the PyROOT objects alive until the canvas is exported.

    def frame(panel, title, x_title, y_title, bounds, *, logy=False):
        pad = canvas.cd(panel)
        pad.SetTopMargin(0.11)
        pad.SetLogy(logy)
        pad.DrawFrame(*bounds, f";{x_title};{y_title}")
        label = ROOT.TLatex()
        ROOT.AtlasStyle.Annotation(label)
        label.DrawLatex(0.16, 0.97, title)

    def graph(x, y):
        curve = ROOT.TGraph(len(x), array("d", x), array("d", y))
        objects.append(curve)
        return curve

    def legend(bounds, entries, columns=1):
        key = ROOT.TLegend(*bounds)
        ROOT.AtlasStyle.Legend(key)
        key.SetNColumns(columns)
        for obj, label, draw_option in entries:
            key.AddEntry(obj, label, draw_option)
        key.Draw()
        objects.append(key)

    frame(1, "Upper limit", "Mass [GeV]", "95% CL upper limit", (285, 0, 715, 3.1))
    mass = [300, 400, 500, 600, 700]
    median = [1.5, 1.1, 0.8, 0.9, 1.0]
    bands = []
    for down, up, preset in (
        (0.4, 0.5, ROOT.AtlasStyle.Expected2Sigma),
        (0.2, 0.2, ROOT.AtlasStyle.Expected1Sigma),
    ):
        band = ROOT.TGraphAsymmErrors(len(mass))
        for i, (x, y) in enumerate(zip(mass, median)):
            band.SetPoint(i, x, y)
            band.SetPointError(i, 0, 0, down * y, up * y)
        preset(band)
        band.Draw("3 SAME")
        bands.append(band)
    expected = graph(mass, median)
    ROOT.AtlasStyle.Expected(expected)
    expected.Draw("L SAME")
    observed = graph(mass, [1.4, 1.2, 0.95, 0.8, 1.1])
    ROOT.AtlasStyle.Data(observed)
    observed.Draw("LP SAME")
    legend((0.43, 0.70, 0.94, 0.88),
           [(observed, "Observed", "lp"), (expected, "Expected", "l"),
            (bands[1], "Expected #pm1#sigma", "f"), (bands[0], "Expected #pm2#sigma", "f")],
           columns=2)

    frame(2, "Likelihood scan", "#kappa", "-2#Delta ln L", (-2, 0, 2, 5))
    x = [-2 + 0.1 * i for i in range(41)]
    observed_scan = graph(x, [(value - 0.2)**2 for value in x])
    ROOT.AtlasStyle.Series(observed_scan, 0)
    observed_scan.Draw("L SAME")
    expected_scan = graph(x, [0.7 * value**2 for value in x])
    ROOT.AtlasStyle.Expected(expected_scan)
    expected_scan.Draw("L SAME")
    reference = ROOT.TLine(-2, 1, 2, 1)
    ROOT.AtlasStyle.Reference(reference)
    reference.Draw()
    legend((0.46, 0.72, 0.73, 0.88),
           [(observed_scan, "Observed", "l"), (expected_scan, "Expected", "l")])

    frame(3, "Efficiency", "p_{T} [GeV]", "Efficiency", (15, 0, 105, 1.05))
    pt = [20, 40, 60, 80, 100]
    simulation = graph(pt, [0.40, 0.68, 0.83, 0.88, 0.91])
    ROOT.AtlasStyle.Series(simulation, 0)
    simulation.Draw("L SAME")
    measured = ROOT.TGraphErrors(len(pt))
    for i, (x, y, error) in enumerate(zip(
        pt, [0.42, 0.67, 0.81, 0.90, 0.92], [0.05, 0.04, 0.03, 0.02, 0.02]
    )):
        measured.SetPoint(i, x, y)
        measured.SetPointError(i, 0, error)
    ROOT.AtlasStyle.Data(measured)
    measured.Draw("P SAME")
    legend((0.64, 0.22, 0.93, 0.39),
           [(measured, "Toy data", "pe"), (simulation, "Simulation", "l")])

    frame(4, "ROC", "Signal efficiency", "Background efficiency",
          (0, 1e-4, 1, 1), logy=True)
    tpr = [0.15 + 0.85 * i / 29 for i in range(30)]
    roc_a = graph(tpr, [value**3 for value in tpr])
    roc_b = graph(tpr, [value**5 for value in tpr])
    ROOT.AtlasStyle.Series(roc_a, 0)
    ROOT.AtlasStyle.Series(roc_b, 1)
    roc_a.Draw("L SAME")
    roc_b.Draw("L SAME")
    legend((0.65, 0.22, 0.93, 0.39), [(roc_a, "Model A", "l"), (roc_b, "Model B", "l")])
    canvas.Print(str(output / "gallery_root.pdf"), "EmbedFonts")

    # Export each matrix before switching ROOT's current palette.
    for name, title, axes, values, preset in (
        ("density", "Response matrix", "Truth bin;Reco bin;Events",
         [[21, 8, 1, 0], [4, 43, 12, 2], [0, 11, 54, 17], [0, 1, 13, 38]],
         ROOT.AtlasStyle.Density),
        ("correlation", "Correlation matrix", "Parameter;Parameter;#rho",
         [[1, 0.62, -0.31, 0.02], [0.62, 1, -0.25, 0.30],
          [-0.31, -0.25, 1, -0.46], [0.02, 0.30, -0.46, 1]],
         ROOT.AtlasStyle.Correlation),
    ):
        pad = ROOT.TCanvas(f"gallery_{name}", "", 750, 650)
        pad.SetRightMargin(0.21)
        pad.SetTopMargin(0.10)
        histogram = ROOT.TH2D(f"matrix_{name}", f";{axes}", 4, -0.5, 3.5, 4, -0.5, 3.5)
        histogram.SetDirectory(0)
        for axis in (histogram.GetXaxis(), histogram.GetYaxis()):
            for index in range(4):
                axis.SetBinLabel(index + 1, str(index))
        for row, entries in enumerate(values, start=1):
            for column, value in enumerate(entries, start=1):
                histogram.SetBinContent(column, row, value)
        preset(histogram)
        histogram.Draw("COLZ")
        label = ROOT.TLatex()
        ROOT.AtlasStyle.Annotation(label)
        label.DrawLatex(0.16, 0.96, title)
        pad.Print(str(output / f"gallery_root_{name}.pdf"), "EmbedFonts")


if __name__ == "__main__":
    main()
