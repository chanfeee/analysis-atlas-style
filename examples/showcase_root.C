#include "../root/AtlasStyle.h"
#include "TCanvas.h"
#include "TGraphErrors.h"
#include "TH1D.h"
#include "TLegend.h"
#include "TLine.h"
#include "TPad.h"
#include "TString.h"
#include "TSystem.h"
#include <array>
#include <cmath>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

// Native ROOT counterpart of showcase_mpl.py; same toy inputs and ratios.
void showcase_root()
{
    ana_atlas_style::use_style();
    const TString source = TString(gSystem->DirName(__FILE__)) + "/showcase_inputs.dat";
    std::ifstream input(source.Data());
    if (!input) throw std::runtime_error("Cannot open showcase_inputs.dat");
    std::vector<std::array<double, 9>> bins;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::istringstream values(line);
        std::array<double, 9> row{};
        for (auto& value : row)
            if (!(values >> value)) throw std::runtime_error("Invalid toy input row");
        bins.push_back(row);
    }
    if (bins.empty()) throw std::runtime_error("No toy input bins");
    const int n = static_cast<int>(bins.size());
    std::vector<double> edges;
    for (const auto& row : bins) edges.push_back(row[0]);
    edges.push_back(bins.back()[1]);

    TCanvas canvas("showcase_canvas", "", 880, 780);
    canvas.SetCanvasSize(880, 780);
    TPad upper("showcase_upper", "", 0, 0.26, 1, 1);
    TPad lower("showcase_lower", "", 0, 0, 1, 0.26);
    upper.SetLeftMargin(0.14);
    upper.SetRightMargin(0.03);
    upper.SetTopMargin(0.05);
    upper.SetBottomMargin(0.015);
    upper.SetLogy();
    lower.SetLeftMargin(0.14);
    lower.SetRightMargin(0.03);
    lower.SetTopMargin(0.025);
    lower.SetBottomMargin(0.34);
    upper.Draw();
    lower.Draw();

    // Cumulative fills give this example explicit control of each stacked area.
    TH1D layer_a("showcase_layer_a", "", n, edges.data());
    TH1D layer_b("showcase_layer_b", "", n, edges.data());
    TH1D layer_c("showcase_layer_c", "", n, edges.data());
    TH1D nominal("showcase_nominal", ";;Events / 10 GeV", n, edges.data());
    TH1D sample("showcase_sample", "", n, edges.data());
    TH1D signal("showcase_signal", "", n, edges.data());
    TH1D alternative("showcase_alternative", "", n, edges.data());
    TH1D ratio("showcase_ratio", ";#it{m} [GeV];Toy / Pred.", n, edges.data());
    TH1D alternative_ratio("showcase_alt_ratio", "", n, edges.data());
    for (auto* hist : {&layer_a, &layer_b, &layer_c, &nominal, &sample, &signal,
                       &alternative, &ratio, &alternative_ratio})
        hist->SetDirectory(nullptr);

    TGraphErrors band(n), ratio_band(n);
    for (int i = 0; i < n; ++i) {
        const auto& row = bins[i];
        const double prediction = row[2] + row[3] + row[4];
        const double center = 0.5 * (row[0] + row[1]);
        const double half_width = 0.5 * (row[1] - row[0]);
        layer_a.SetBinContent(i + 1, prediction);
        layer_b.SetBinContent(i + 1, row[3] + row[4]);
        layer_c.SetBinContent(i + 1, row[4]);
        nominal.SetBinContent(i + 1, prediction);
        sample.SetBinContent(i + 1, row[6]);
        sample.SetBinError(i + 1, std::sqrt(row[6]));
        signal.SetBinContent(i + 1, 4 * row[5]);
        alternative.SetBinContent(i + 1, row[8]);
        ratio.SetBinContent(i + 1, row[6] / prediction);
        // Numerator statistics only; denominator uncertainty is the band.
        ratio.SetBinError(i + 1, std::sqrt(row[6]) / prediction);
        alternative_ratio.SetBinContent(i + 1, row[8] / prediction);
        band.SetPoint(i, center, prediction);
        band.SetPointError(i, half_width, row[7]);
        ratio_band.SetPoint(i, center, 1);
        ratio_band.SetPointError(i, half_width, row[7] / prediction);
    }

    ana_atlas_style::Background(layer_a, 0);
    ana_atlas_style::Background(layer_b, 1);
    ana_atlas_style::Background(layer_c, 2);
    ana_atlas_style::Prediction(nominal);
    ana_atlas_style::Data(sample);
    ana_atlas_style::Signal(signal);
    ana_atlas_style::Alternative(alternative);
    ana_atlas_style::Uncertainty(band);
    ana_atlas_style::Uncertainty(ratio_band);
    TGraphErrors band_shade(band);
    ana_atlas_style::UncertaintyShade(band_shade);

    upper.cd();
    nominal.SetMinimum(0.6);
    nominal.SetMaximum(60000);
    nominal.GetXaxis()->SetLabelSize(0);
    nominal.GetYaxis()->SetLabelFont(43);
    nominal.GetYaxis()->SetLabelSize(21);
    nominal.GetYaxis()->SetTitleFont(43);
    nominal.GetYaxis()->SetTitleSize(26);
    nominal.GetYaxis()->SetTitleOffset(1.35);
    nominal.Draw("AXIS");
    layer_a.Draw("HIST SAME");
    layer_b.Draw("HIST SAME");
    layer_c.Draw("HIST SAME");
    band_shade.Draw("2 SAME");
    band.Draw("2 SAME");
    nominal.Draw("HIST SAME");
    alternative.Draw("HIST SAME");
    signal.Draw("HIST SAME");
    sample.Draw("E1 X0 SAME");

    auto* atlas = ana_atlas_style::AtlasLabel(0.18, 0.90, "Simulation");
    atlas->SetTextSize(0.045);
    TLatex text;
    text.SetNDC();
    text.SetTextFont(43);
    text.SetTextAlign(13);
    text.SetTextSize(21);
    text.DrawLatex(0.18, 0.835, "#sqrt{s} = 13 TeV, 140 fb^{-1}");
    ana_atlas_style::Annotation(text);
    text.SetTextFont(43);  // Pixel font for this multi-pad layout.
    text.SetTextSize(19);
    text.DrawLatex(0.18, 0.765, "Toy inputs - illustrative region");
    TLegend legend(0.53, 0.715, 0.965, 0.91);
    ana_atlas_style::Legend(legend);
    legend.SetNColumns(2);
    legend.SetTextFont(43);
    legend.SetTextSize(18);
    // ROOT fills legend entries row by row.
    legend.AddEntry(&sample, "Toy sample", "pe");
    legend.AddEntry(&layer_a, "Background A", "f");
    legend.AddEntry(&nominal, "Total pred.", "l");
    legend.AddEntry(&layer_b, "Background B", "f");
    legend.AddEntry(&alternative, "Alt. model", "l");
    legend.AddEntry(&layer_c, "Background C", "f");
    legend.AddEntry(&signal, "Signal #times 4", "l");
    legend.AddEntry(&band, "Total unc.", "f");
    legend.Draw();
    upper.RedrawAxis();

    lower.cd();
    ratio.SetMinimum(0.65);
    ratio.SetMaximum(1.35);
    ana_atlas_style::Data(ratio);
    for (auto* axis : {ratio.GetXaxis(), ratio.GetYaxis()}) {
        axis->SetLabelFont(43);
        axis->SetLabelSize(21);
        axis->SetTitleFont(43);
        axis->SetTitleSize(26);
    }
    ratio.GetXaxis()->SetNdivisions(508);
    ratio.GetXaxis()->SetTitleOffset(1.15);
    ratio.GetYaxis()->SetNdivisions(504);
    ratio.GetYaxis()->SetTitleSize(23);
    ratio.GetYaxis()->SetTitleOffset(1.6);
    ratio.GetYaxis()->CenterTitle();
    ratio.Draw("AXIS");
    ratio_band.Draw("2 SAME");
    TLine unity(edges.front(), 1, edges.back(), 1);
    ana_atlas_style::Reference(unity);
    unity.Draw();
    ana_atlas_style::Alternative(alternative_ratio);
    alternative_ratio.SetLineWidth(2);  // Local override; native setters win.
    alternative_ratio.Draw("HIST SAME");
    ratio.Draw("E1 X0 SAME");
    lower.RedrawAxis();
    canvas.cd();
    canvas.Update();
    const TString output = TString(gSystem->DirName(__FILE__)) + "/output";
    gSystem->mkdir(output.Data(), true);
    canvas.Print((output + "/showcase_root.pdf").Data(), "EmbedFonts");
}
