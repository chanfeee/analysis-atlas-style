#ifndef ANA_ATLAS_STYLE_H
#define ANA_ATLAS_STYLE_H

// Local ATLAS style implementation, using the public ATLAS style parameters.
// Parameter reference and provenance: ../README.md (Sources).
// This header is not an unmodified upstream AtlasStyle distribution.

#include <string>
#include "TLatex.h"
#include "TROOT.h"
#include "TStyle.h"
#include "AtlasArtists.h"

namespace ana_atlas_style {
inline TStyle* use_style()
{
    static TStyle* style = nullptr;
    if (!style) {
        style = new TStyle("ana_atlas_style", "ATLAS publication style");
        style->SetFrameBorderMode(0);
        style->SetFrameFillColor(0);
        style->SetCanvasBorderMode(0);
        style->SetCanvasColor(0);
        style->SetCanvasDefW(800);
        style->SetCanvasDefH(600);
        style->SetPadBorderMode(0);
        style->SetPadColor(0);
        style->SetStatColor(0);
        style->SetPaperSize(20, 26);
        style->SetPadTopMargin(0.05);
        style->SetPadRightMargin(0.05);
        style->SetPadBottomMargin(0.16);
        style->SetPadLeftMargin(0.16);
        style->SetTitleXOffset(1.4);
        style->SetTitleYOffset(1.4);
        style->SetTextFont(42);
        style->SetTextSize(0.05);
        style->SetLabelFont(42, "XYZ");
        style->SetTitleFont(42, "XYZ");
        style->SetLabelSize(0.05, "XYZ");
        style->SetTitleSize(0.05, "XYZ");
        style->SetMarkerStyle(20);
        style->SetMarkerSize(0.8);
        style->SetMarkerColor(colors::Data());
        style->SetHistLineColor(colors::Prediction());
        style->SetHistLineStyle(1);
        style->SetHistLineWidth(2);
        style->SetHistFillStyle(0);
        style->SetLineWidth(1);
        // ROOT's dash units differ from Matplotlib points. Keep long signal
        // dashes distinct from the shorter alternative and reference dashes.
        style->SetLineStyleString(2, "[48 16]");
        style->SetLineStyleString(7, "[24 16]");
        style->SetLineStyleString(3, "[16 16]");
        style->SetHatchesLineWidth(1);
        style->SetHatchesSpacing(1);
        style->SetEndErrorSize(0);
        style->SetOptTitle(0);
        style->SetOptStat(0);
        style->SetOptFit(0);
        style->SetPadTickX(1);
        style->SetPadTickY(1);
        style->SetPadGridX(false);
        style->SetPadGridY(false);
        style->SetLegendBorderSize(0);
        style->SetLegendFillColor(0);
        style->SetLegendFont(42);
        style->SetLegendTextSize(0.04);
    }
    style->cd();
    // Do not enable ForceStyle when reading objects. Saving never reapplies
    // this style; individual object attributes stay caller-owned.
    return style;
}

inline TStyle* SetAtlasStyle()
{
    return use_style();
}

inline TLatex* AtlasLabel(double x, double y, const char* text = "")
{
    // x and y are pad NDC coordinates; y anchors the top of the label.
    TLatex label;
    label.SetNDC();
    label.SetTextFont(42);
    label.SetTextSize(gStyle->GetTextSize());
    label.SetTextAlign(13);
    std::string title = "#font[72]{ATLAS}";
    if (text && *text) title += std::string(" #font[42]{") + text + "}";
    return label.DrawLatex(x, y, title.c_str());
}

} // namespace ana_atlas_style

#endif
