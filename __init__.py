"""Public ATLAS style API, with no backend imports or style changes on import.

Figure layout, data processing and native drawing calls belong to the caller.
"""

from .colors import (
    BACKGROUND_COLORS,
    BACKGROUND_FILL_COLORS,
    COLORS,
    FILL_COLORS,
    SERIES_COLORS,
    SERIES_FILL_COLORS,
)
from .mpl import artist_style, atlas_label, atlas_style, matrix_style, use_atlas_style
from .root import root_include_dir, use_root_style

__version__ = "0.2.0"


def use_style(backend="mpl", **options):
    """Apply ATLAS defaults before creating native drawing objects.

    The Matplotlib backend accepts font and rc options. ROOT returns a TStyle
    that the caller can customize directly.
    """
    if backend == "mpl":
        return use_atlas_style(**options)
    if backend == "root":
        return use_root_style(**options)
    raise ValueError(f"Unknown style backend {backend!r}; choose 'mpl' or 'root'")


__all__ = [
    "__version__",
    "use_style",
    "use_atlas_style",
    "atlas_style",
    "atlas_label",
    "artist_style",
    "matrix_style",
    "use_root_style",
    "root_include_dir",
    "COLORS",
    "FILL_COLORS",
    "SERIES_COLORS",
    "SERIES_FILL_COLORS",
    "BACKGROUND_COLORS",
    "BACKGROUND_FILL_COLORS",
]
