#ifndef ANALYSIS_BASE_ATLAS_COLORS_H
#define ANALYSIS_BASE_ATLAS_COLORS_H

#include "TColor.h"

// Keep these defaults consistent with ../colors.py.
// Role assignments are local conventions; they are not ATLAS-wide rules.
// Accents: ggsci NEJM-inspired palette. Fills: 45% accent + 55% white.
namespace AtlasColors {
inline Color_t Data()        { return TColor::GetColor("#000000"); }
inline Color_t Prediction()  { return TColor::GetColor("#303030"); }
inline Color_t Signal()      { return TColor::GetColor("#BC3C29"); }
inline Color_t Background()  { return TColor::GetColor("#0072B5"); }
inline Color_t Alternative() { return TColor::GetColor("#7876B1"); }
inline Color_t Uncertainty() { return TColor::GetColor("#999999"); }
inline Color_t Reference()   { return TColor::GetColor("#404040"); }
inline Color_t Annotation()  { return TColor::GetColor("#444444"); }

inline Color_t Series(unsigned int index)
{
    static const char* hex[] = {
        "#0072B5", "#BC3C29", "#20854E", "#E18727", "#7876B1"
    };
    const unsigned int count = sizeof(hex) / sizeof(hex[0]);
    return TColor::GetColor(hex[index % count]);
}

inline Color_t SeriesFill(unsigned int index)
{
    static const char* hex[] = {
        "#8CC0DE", "#E1A79F", "#9BC8AF", "#F2C99E", "#C2C1DC"
    };
    const unsigned int count = sizeof(hex) / sizeof(hex[0]);
    return TColor::GetColor(hex[index % count]);
}

inline Color_t PredictionFill()  { return TColor::GetColor("#A2A2A2"); }
inline Color_t SignalFill()      { return SeriesFill(1); }
inline Color_t BackgroundFill()  { return SeriesFill(0); }
inline Color_t AlternativeFill() { return SeriesFill(4); }
} // namespace AtlasColors

#endif
