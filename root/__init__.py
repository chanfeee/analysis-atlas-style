"""ROOT header discovery and opt-in PyROOT initialization."""

from pathlib import Path

__all__ = ["root_include_dir", "use_root_style"]


def root_include_dir():
    """Return the installed directory containing the standalone C++ headers."""
    return Path(__file__).resolve().parent


def use_root_style():
    """Load the bundled headers, apply defaults and return the native TStyle.

    PyROOT is imported only here and must be installed by the caller. Native
    ROOT objects, attributes and ownership stay under the caller's control.
    """
    try:
        import ROOT
    except ModuleNotFoundError as exc:
        if exc.name != "ROOT":
            raise
        raise ModuleNotFoundError(
            "PyROOT is unavailable in this Python environment. Activate an "
            "environment with ROOT installed before calling use_root_style().",
            name="ROOT",
        ) from exc

    header = root_include_dir() / "AtlasStyle.h"
    if not header.is_file():
        raise FileNotFoundError(f"Bundled ROOT style header is missing: {header}")
    if not ROOT.gInterpreter.Declare(f'#include "{header.as_posix()}"'):
        raise RuntimeError(f"ROOT could not load the bundled style: {header}")
    return ROOT.ana_atlas_style.use_style()
