#ifndef ANALYSIS_BASE_ATLAS_ARTISTS_H
#define ANALYSIS_BASE_ATLAS_ARTISTS_H

#include "AtlasColors.h"
#include "TStyle.h"

// Attribute presets only: no Draw, data access, error calculation or ownership.
// Apply a preset first, then use any native Set... methods to override it.
namespace AtlasStyle {
template <class T> inline T& Data(T& object)
{
    object.SetLineColor(AtlasColors::Data());
    object.SetLineStyle(1);
    object.SetLineWidth(1);
    object.SetMarkerColor(AtlasColors::Data());
    object.SetMarkerStyle(20);
    object.SetMarkerSize(0.8);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Prediction(T& object)
{
    object.SetLineColor(AtlasColors::Prediction());
    object.SetLineStyle(1);
    object.SetLineWidth(2);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Signal(T& object)
{
    object.SetLineColor(AtlasColors::Signal());
    object.SetLineStyle(2);
    object.SetLineWidth(3);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Alternative(T& object)
{
    object.SetLineColor(AtlasColors::Alternative());
    object.SetLineStyle(7);
    object.SetLineWidth(3);
    object.SetFillStyle(0);
    return object;
}

template <class T> inline T& Background(T& object, unsigned int index = 0)
{
    object.SetLineColor(AtlasColors::Series(index));
    object.SetLineStyle(1);
    object.SetLineWidth(1);
    object.SetFillColor(AtlasColors::SeriesFill(index));
    object.SetFillStyle(1001);
    return object;
}

template <class T> inline T& Uncertainty(T& object)
{
    object.SetFillColor(AtlasColors::Uncertainty());
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
    object.SetLineColor(AtlasColors::Reference());
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
    object.SetTextColor(AtlasColors::Annotation());
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
} // namespace AtlasStyle

#endif
