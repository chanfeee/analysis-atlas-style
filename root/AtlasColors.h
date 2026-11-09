#ifndef ANA_ATLAS_STYLE_COLORS_H
#define ANA_ATLAS_STYLE_COLORS_H

#include "TColor.h"
#include "TError.h"

// Keep these defaults consistent with ../colors.py.
// Role assignments are local conventions; they are not ATLAS-wide rules.
// Sources: PRL 132, 221801, Fig. 2 and PRL 133, 101801, Fig. 2.
namespace ana_atlas_style::colors {
inline Color_t Data()        { return TColor::GetColor("#000000"); }
inline Color_t Prediction()  { return TColor::GetColor("#333333"); }
inline Color_t Signal()      { return TColor::GetColor("#6A51A3"); }
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

inline Color_t Background(unsigned int index = 0)
{
    static const char* hex[] = {
        "#33395B", "#5D74A2", "#C4D8F2", "#8E2D30",
        "#82AD92", "#CFAB66", "#AB99C6", "#F2E8E3"
    };
    const unsigned int count = sizeof(hex) / sizeof(hex[0]);
    if (index >= count) {
        ::Error("ana_atlas_style::colors::Background",
                "background index %u exceeds the default palette; set native colors", index);
        return -1;
    }
    return TColor::GetColor(hex[index]);
}

inline Color_t BackgroundFill(unsigned int index = 0)
{
    return Background(index);
}

inline Color_t PredictionFill()  { return SeriesFill(3); }
inline Color_t SignalFill()      { return SeriesFill(1); }
inline Color_t AlternativeFill() { return SeriesFill(4); }
} // namespace ana_atlas_style::colors

#endif
