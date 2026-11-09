#ifndef ANALYSIS_BASE_ATLAS_COLORS_H
#define ANALYSIS_BASE_ATLAS_COLORS_H

#include "TColor.h"

// Keep these defaults consistent with ../colors.py.
// Role assignments are local conventions; they are not ATLAS-wide rules.
// Sources: PRL 132, 221801, Fig. 2 and PRL 133, 101801, Fig. 2.
namespace AtlasColors {
inline Color_t Data()        { return TColor::GetColor("#000000"); }
inline Color_t Prediction()  { return TColor::GetColor("#333333"); }
inline Color_t Signal()      { return TColor::GetColor("#6A51A3"); }
inline Color_t Background()  { return TColor::GetColor("#4292C6"); }
inline Color_t Alternative() { return TColor::GetColor("#FF7700"); }
inline Color_t Uncertainty() { return TColor::GetColor("#666666"); }
inline Color_t Reference()   { return TColor::GetColor("#404040"); }
inline Color_t Expected1Sigma() { return TColor::GetColor("#4AD9D9"); }
inline Color_t Expected2Sigma() { return TColor::GetColor("#FDC536"); }
inline Color_t Annotation()  { return TColor::GetColor("#444444"); }

inline Color_t Series(unsigned int index)
{
    static const char* hex[] = {
        "#4292C6", "#6A51A3", "#278471", "#666666", "#FF7700"
    };
    const unsigned int count = sizeof(hex) / sizeof(hex[0]);
    return TColor::GetColor(hex[index % count]);
}

inline Color_t SeriesFill(unsigned int index)
{
    static const char* hex[] = {
        "#BCE1FF", "#BCB1D6", "#48C9B0", "#D6D6D6", "#FFC28C"
    };
    const unsigned int count = sizeof(hex) / sizeof(hex[0]);
    return TColor::GetColor(hex[index % count]);
}

inline Color_t PredictionFill()  { return SeriesFill(3); }
inline Color_t SignalFill()      { return SeriesFill(1); }
inline Color_t BackgroundFill()  { return SeriesFill(0); }
inline Color_t AlternativeFill() { return SeriesFill(4); }
} // namespace AtlasColors

#endif
