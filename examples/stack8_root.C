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
#include <memory>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

// Native ROOT counterpart of stack8_mpl.py with the same deterministic toy inputs.
void stack8_root()
{
    namespace style = ana_atlas_style;
    style::use_style();
    const TString directory(gSystem->DirName(__FILE__));
    std::ifstream input((directory + "/stack8_inputs.dat").Data());
    if (!input) throw std::runtime_error("Cannot open stack8_inputs.dat");
    std::vector<std::array<double, 14>> bins;
    for (std::string line; std::getline(input, line);) {
        if (line.empty() || line[0] == '#') continue;
        std::istringstream values(line);
        std::array<double, 14> row{};
        for (auto& value : row)
            if (!(values >> value)) throw std::runtime_error("Invalid stack8 input row");
        bins.push_back(row);
    }
    if (bins.empty()) throw std::runtime_error("No stack8 toy input bins");

    const int n = static_cast<int>(bins.size());
    std::vector<double> edges;
    for (const auto& row : bins) edges.push_back(row[0]);
    edges.push_back(bins.back()[1]);
    const std::array<const char*, 8> labels = {
        "t#bar{t}", "W+jets", "Z+jets", "Single top", "Diboson", "t#bar{t}+V", "Multijet", "Other"
    };
    std::array<std::unique_ptr<TH1D>, labels.size()> components;
    for (unsigned int j = 0; j < components.size(); ++j) {
        components[j] = std::make_unique<TH1D>(Form("stack8_background_%u", j), "", n, edges.data());
        auto& histogram = *components[j];
        histogram.SetDirectory(nullptr);
        style::Background(histogram, j);
        for (int i = 0; i < n; ++i)
            histogram.SetBinContent(i + 1, std::accumulate(bins[i].begin() + 2 + j,
                                                          bins[i].begin() + 10, 0.));
    }

    TH1D nominal("stack8_nominal", ";;Events / 10 GeV", n, edges.data());
    TH1D alternate("stack8_alternate", "", n, edges.data());
    TH1D signal("stack8_signal", "", n, edges.data());
    TH1D altRatio("stack8_alt_ratio", "", n, edges.data());
    TH1D ratioFrame("stack8_ratio_frame", ";#it{m}_{jj} [GeV];Data / Pred.", n, edges.data());
    for (auto* histogram : {&nominal, &alternate, &signal, &altRatio, &ratioFrame})
        histogram->SetDirectory(nullptr);
    TGraphErrors data(n), ratio(n), band(n), ratioBand(n);
    for (int i = 0; i < n; ++i) {
        const auto& row = bins[i];
        const double prediction = components.front()->GetBinContent(i + 1);
        const double center = (row[0] + row[1]) / 2;
        const double halfWidth = (row[1] - row[0]) / 2;
        const double observed = row[10], relativeUnc = row[12];
        const double stat = std::sqrt(observed);
        nominal.SetBinContent(i + 1, prediction);
        signal.SetBinContent(i + 1, row[11]);
        alternate.SetBinContent(i + 1, row[13] * prediction);
        altRatio.SetBinContent(i + 1, row[13]);
        data.SetPoint(i, center, observed);
        data.SetPointError(i, 0, stat);
        band.SetPoint(i, center, prediction);
        band.SetPointError(i, halfWidth, relativeUnc * prediction);
        ratio.SetPoint(i, center, observed / prediction);
        ratio.SetPointError(i, 0, stat / prediction);
        ratioBand.SetPoint(i, center, 1);
        ratioBand.SetPointError(i, halfWidth, relativeUnc);
    }
    style::Prediction(nominal);
    style::Signal(signal);
    style::Alternative(alternate);
    style::Alternative(altRatio);
    altRatio.SetLineWidth(2);
    style::Data(data);
    style::Data(ratio);
    style::Uncertainty(band);
    style::Uncertainty(ratioBand);
    TGraphErrors shade(band);
    style::UncertaintyShade(shade);

    TCanvas canvas("stack8_canvas", "", 880, 780);
    canvas.SetCanvasSize(880, 780);
    TPad upper("stack8_upper", "", 0, 0.28, 1, 1);
    TPad lower("stack8_lower", "", 0, 0, 1, 0.28);
    for (auto* pad : {&upper, &lower}) {
        pad->SetLeftMargin(0.14);
        pad->SetRightMargin(0.03);
        pad->Draw();
    }
    upper.SetTopMargin(0.07);
    upper.SetBottomMargin(0.015);
    upper.SetLogy();
    lower.SetTopMargin(0.045);
    lower.SetBottomMargin(0.43);
    auto formatAxis = [](TAxis& axis, int labelSize, int titleSize) {
        axis.SetLabelFont(43);
        axis.SetLabelSize(labelSize);
        axis.SetTitleFont(43);
        axis.SetTitleSize(titleSize);
    };

    upper.cd();
    nominal.SetMinimum(6);
    nominal.SetMaximum(32000);
    nominal.GetXaxis()->SetLabelSize(0);
    nominal.GetXaxis()->SetNdivisions(508);
    formatAxis(*nominal.GetYaxis(), 21, 26);
    nominal.GetYaxis()->SetTitleOffset(1.35);
    nominal.Draw("AXIS");
    // Paint cumulative fills from the total down to the bottom layer.
    for (const auto& histogram : components) histogram->Draw("HIST SAME");
    shade.Draw("2 SAME");
    band.Draw("2 SAME");
    nominal.Draw("HIST SAME");
    alternate.Draw("HIST SAME");
    signal.Draw("HIST SAME");
    data.Draw("P SAME");

    style::AtlasLabel(0.17, 0.885, "Simulation");
    TLatex text;
    text.SetNDC();
    text.SetTextAlign(13);
    text.SetTextFont(43);
    text.SetTextSize(21);
    text.DrawLatex(0.17, 0.823, "#sqrt{s} = 13 TeV, 140 fb^{-1}");
    style::Annotation(text);
    text.SetTextFont(43);
    text.SetTextSize(18);
    text.DrawLatex(0.17, 0.72, "Toy validation region");
    TLegend legend(0.62, 0.62, 0.96, 0.91);
    style::Legend(legend);
    legend.SetTextFont(43);
    legend.SetTextSize(15.5);
    legend.SetNColumns(2);
    std::array<TObject*, 5> overlays = {&data, &nominal, &alternate, &signal, &band};
    const std::array<const char*, 5> overlayLabels = {
        "Pseudo-data", "Total pred.", "Alt. model", "Toy signal", "Total unc."
    };
    const std::array<const char*, 5> options = {"pe", "l", "l", "l", "f"};
    for (unsigned int row = 0; row < 7; ++row) {
        if (row < overlays.size()) legend.AddEntry(overlays[row], overlayLabels[row], options[row]);
        else legend.AddEntry(components[row - overlays.size()].get(), labels[row - overlays.size()], "f");
        if (row + 2 < labels.size()) legend.AddEntry(components[row + 2].get(), labels[row + 2], "f");
    }
    legend.Draw();
    upper.RedrawAxis();

    lower.cd();
    ratioFrame.SetMinimum(0.7);
    ratioFrame.SetMaximum(1.3);
    auto& xAxis = *ratioFrame.GetXaxis();
    auto& yAxis = *ratioFrame.GetYaxis();
    formatAxis(xAxis, 21, 26);
    formatAxis(yAxis, 21, 19);
    xAxis.SetNdivisions(508);
    xAxis.SetTitleOffset(1.28);
    yAxis.SetNdivisions(504);
    yAxis.SetTitleOffset(1.7);
    yAxis.CenterTitle();
    ratioFrame.Draw("AXIS");
    ratioBand.Draw("2 SAME");
    TLine unity(edges.front(), 1, edges.back(), 1);
    style::Reference(unity);
    unity.Draw();
    altRatio.Draw("HIST SAME");
    ratio.Draw("P SAME");
    lower.RedrawAxis();

    canvas.cd();
    canvas.Update();
    const TString output = directory + "/output";
    gSystem->mkdir(output.Data(), true);
    canvas.Print((output + "/stack8_root.pdf").Data(), "EmbedFonts");
}
