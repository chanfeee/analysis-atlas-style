#ifndef ANA_ATLAS_STYLE_ARTISTS_H
#define ANA_ATLAS_STYLE_ARTISTS_H

#include <array>
#include <numeric>
#include "AtlasColors.h"
#include "TROOT.h"
#include "TStyle.h"

// Attribute presets only: no Draw, data access, error calculation or ownership.
// Apply a preset first, then use any native Set... methods to override it.
namespace ana_atlas_style {
template <class T> inline T& Data(T& object)
{
    object.SetLineColor(colors::Data());
    object.SetLineStyle(1);
    object.SetLineWidth(1);
    object.SetMarkerColor(colors::Data());
    object.SetMarkerStyle(20);
    object.SetMarkerSize(0.8);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Prediction(T& object)
{
    object.SetLineColor(colors::Prediction());
    object.SetLineStyle(1);
    object.SetLineWidth(2);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Signal(T& object)
{
    object.SetLineColor(colors::Signal());
    object.SetLineStyle(2);
    object.SetLineWidth(3);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Alternative(T& object)
{
    object.SetLineColor(colors::Alternative());
    object.SetLineStyle(7);
    object.SetLineWidth(3);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Background(T& object, unsigned int index = 0)
{
    const Color_t color = colors::Background(index);
    if (color < 0) return object;
    object.SetLineColor(color);
    object.SetLineStyle(1);
    object.SetLineWidth(1);
    object.SetFillColor(color);
    object.SetFillStyle(1001);
    return object;
}

template <class T> inline T& Series(T& object, unsigned int index = 0)
{
    static const Style_t lineStyles[] = {1, 2, 7, 3};
    object.SetLineColor(colors::Series(index));
    object.SetLineStyle(lineStyles[index % 4]);
    object.SetLineWidth(3);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Expected(T& object)
{
    object.SetLineColor(colors::Data());
    object.SetLineStyle(3);
    object.SetLineWidth(2);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Expected1Sigma(T& object)
{
    object.SetFillColor(colors::Expected1Sigma());
    object.SetFillStyle(1001);
    object.SetLineWidth(0);
    return object;
}

template <class T> inline T& Expected2Sigma(T& object)
{
    object.SetFillColor(colors::Expected2Sigma());
    object.SetFillStyle(1001);
    object.SetLineWidth(0);
    return object;
}

namespace detail {
constexpr int MatrixContours = 255;

template <std::size_t N> inline int CreatePalette(const char* const (&hex)[N])
{
    std::array<Double_t, N> stops, red, green, blue;
    for (std::size_t i = 0; i < N; ++i) {
        const TColor* color = gROOT->GetColor(TColor::GetColor(hex[i]));
        stops[i] = static_cast<double>(i) / (N - 1);
        red[i] = color->GetRed();
        green[i] = color->GetGreen();
        blue[i] = color->GetBlue();
    }
    return TColor::CreateGradientColorTable(N, stops.data(), red.data(), green.data(),
                                            blue.data(), MatrixContours, 1., false);
}

inline void SetPalette(int firstColor)
{
    std::array<Int_t, MatrixContours> indices;
    std::iota(indices.begin(), indices.end(), firstColor);
    gStyle->SetPalette(MatrixContours, indices.data());
}
} // namespace detail

template <class T> inline T& Density(T& histogram)
{
    // Keep the RGB stops in sync with colors.py.
    static const char* hex[] = {"#FFFFFF", "#BCE1FF", "#4292C6", "#174568"};
    static const int firstColor = detail::CreatePalette(hex);
    detail::SetPalette(firstColor);
    histogram.SetContour(detail::MatrixContours);
    return histogram;
}

template <class T> inline T& Correlation(T& histogram)
{
    static const char* hex[] = {"#2166AC", "#FFFFFF", "#C62F3B"};
    static const int firstColor = detail::CreatePalette(hex);
    detail::SetPalette(firstColor);
    histogram.SetContour(detail::MatrixContours);
    histogram.SetMinimum(-1);
    histogram.SetMaximum(1);
    return histogram;
}

template <class T> inline T& Uncertainty(T& object)
{
    object.SetFillColor(colors::Uncertainty());
    object.SetFillStyle(3004);
    object.SetLineWidth(0);
    return object;
}

// Optional white backing for a hatch over a colored stack. Draw the backing
// and the hatched band separately with the native ROOT calls, in that order.
template <class T> inline T& UncertaintyShade(T& object)
{
    object.SetFillColorAlpha(kWhite, 0.65);
    object.SetFillStyle(1001);
    object.SetLineWidth(0);
    return object;
}

template <class T> inline T& Reference(T& object)
{
    object.SetLineColor(colors::Reference());
    object.SetLineStyle(3);
    object.SetLineWidth(1);
    return object;
}

template <class T> inline T& Annotation(T& object)
{
    object.SetNDC();
    object.SetTextFont(42);
    object.SetTextSize(0.04);
    object.SetTextAlign(13);
    object.SetTextColor(colors::Annotation());
    return object;
}

template <class T> inline T& Legend(T& object)
{
    object.SetBorderSize(gStyle->GetLegendBorderSize());
    object.SetFillStyle(0);
    object.SetTextFont(gStyle->GetLegendFont());
    object.SetTextSize(gStyle->GetLegendTextSize());
    return object;
}
} // namespace ana_atlas_style

#endif
