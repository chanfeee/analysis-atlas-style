"""Public ATLAS style API, with no backend imports or style changes on import.

Figure layout, data processing and native drawing calls belong to the caller.
"""

from .colors import COLORS, FILL_COLORS, SERIES_COLORS, SERIES_FILL_COLORS
from .mpl import artist_style, atlas_label, atlas_style, matrix_style, use_atlas_style
from .root import root_include_dir, use_root_style

__version__ = "0.1.0"

__all__ = [
    "__version__",
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
]
