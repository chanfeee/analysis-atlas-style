#include "../root/AtlasStyle.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TH1D.h"
#include "TGraphErrors.h"
#include "TLegend.h"
#include "TString.h"
#include "TSystem.h"
#include <cmath>

void atlas_root()
{
    SetAtlasStyle();
    TCanvas canvas("atlas_example", "", 800, 600);
    canvas.SetCanvasSize(800, 600);
    TH1D sample("atlas_toy_sample", ";#it{m} [GeV];Events / 10 GeV", 10, 60, 160);
    TH1D expected("atlas_toy_expected", "", 10, 60, 160);
    TH1D signal("atlas_toy_signal", "", 10, 60, 160);
    sample.SetDirectory(nullptr);
    expected.SetDirectory(nullptr);
    signal.SetDirectory(nullptr);
    TGraphErrors band(10);
    const double counts[] = {10, 26, 70, 125, 92, 53, 26, 14, 8, 3};
    const double model[] = {12, 25, 65, 115, 100, 50, 28, 16, 7, 4};
    const double signal_counts[] = {0, 0, 1, 5, 12, 22, 12, 5, 1, 0};
    for (int i = 0; i < 10; ++i) {
        sample.SetBinContent(i + 1, counts[i]);
        sample.SetBinError(i + 1, std::sqrt(counts[i]));
        expected.SetBinContent(i + 1, model[i]);
        signal.SetBinContent(i + 1, signal_counts[i]);
        // Illustrative toy input, not an uncertainty prescription.
        band.SetPoint(i, 65 + 10 * i, model[i]);
        band.SetPointError(i, 5, 0.1 * model[i]);
    }
    sample.SetMinimum(0);
    sample.SetMaximum(190);
    AtlasStyle::Data(sample);
    AtlasStyle::Uncertainty(band);
    AtlasStyle::Prediction(expected);
    AtlasStyle::Signal(signal);
    sample.Draw("E1 X0");
    band.Draw("2 SAME");
    expected.Draw("HIST SAME");
    signal.Draw("HIST SAME");
    sample.Draw("E1 X0 SAME");

    AtlasLabel(0.20, 0.89, "Simulation");
    TLatex info;
    info.SetNDC();
    info.SetTextFont(42);
    info.SetTextSize(0.04);
    info.DrawLatex(0.20, 0.79, "#sqrt{s} = 13 TeV");
    TLegend legend(0.62, 0.64, 0.94, 0.90);
    AtlasStyle::Legend(legend);
    legend.AddEntry(&sample, "Toy sample", "pe");
    legend.AddEntry(&expected, "Toy prediction", "l");
    legend.AddEntry(&band, "Toy uncertainty", "f");
    legend.AddEntry(&signal, "Toy signal", "l");
    legend.Draw();
    canvas.RedrawAxis();

    const TString output = TString(gSystem->DirName(__FILE__)) + "/output";
    gSystem->mkdir(output.Data(), true);
    // ROOT's native embedding option requires Ghostscript (gs) on PATH.
    canvas.Print((output + "/atlas_root.pdf").Data(), "EmbedFonts");
}
