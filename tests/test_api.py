"""Boundary checks for the style package; plotting backends are optional."""

from importlib.util import find_spec
from io import BytesIO
from pathlib import Path
import copy
import subprocess
import sys
import unittest

import ana_atlas_style


class PublicAPITests(unittest.TestCase):
    def test_import_does_not_load_backends(self):
        result = subprocess.run(
            [sys.executable, "-c", (
                "import sys, ana_atlas_style; "
                "assert not {'matplotlib', 'mplhep', 'ROOT'} & sys.modules.keys(); "
                "assert callable(ana_atlas_style.artist_style); "
                "assert callable(ana_atlas_style.use_root_style)"
            )],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_cli_finds_the_bundled_headers(self):
        result = subprocess.run(
            [sys.executable, "-m", "ana_atlas_style", "--root-include"],
            capture_output=True, text=True, check=True,
        )
        directory = Path(result.stdout.strip())
        self.assertEqual(directory, ana_atlas_style.root_include_dir())
        for name in ("AtlasStyle.h", "AtlasArtists.h", "AtlasColors.h"):
            self.assertTrue((directory / name).is_file(), name)


@unittest.skipUnless(find_spec("matplotlib") and find_spec("mplhep"), "Matplotlib extra is absent")
class MatplotlibTests(unittest.TestCase):
    def test_manual_overrides_survive_export_and_context_is_restored(self):
        import matplotlib as mpl
        mpl.use("Agg")
        import matplotlib.pyplot as plt

        before = copy.deepcopy(dict(mpl.rcParams))
        with ana_atlas_style.atlas_style(rc={"lines.linewidth": 3.25}):
            fig, ax = plt.subplots()
            try:
                plain, = ax.plot([0, 1], [1, 2])
                self.assertEqual(plain.get_linewidth(), 3.25)
                signal = ax.stairs(
                    [1, 2], [0, 1, 2],
                    **ana_atlas_style.artist_style("signal", color="magenta", linewidth=2.5),
                )
                signal.set_linewidth(4)
                signal.set_linestyle("-")
                ax.set_xlim(-1, 3)
                fig.savefig(BytesIO(), format="svg")
                self.assertEqual(signal.get_linewidth(), 4)
                self.assertEqual(signal.get_linestyle(), "-")
                self.assertEqual(signal.get_edgecolor()[:3], (1, 0, 1))
                self.assertEqual(ax.get_xlim(), (-1, 3))
            finally:
                plt.close(fig)
        self.assertEqual(dict(mpl.rcParams), before)

        with self.assertRaises(RuntimeError):
            with ana_atlas_style.atlas_style(rc={"lines.linewidth": 8}):
                raise RuntimeError("exercise context cleanup")
        self.assertEqual(dict(mpl.rcParams), before)


@unittest.skipUnless(find_spec("ROOT"), "PyROOT is absent")
class RootTests(unittest.TestCase):
    def test_packaged_headers_load_and_native_overrides_work(self):
        import ROOT

        original_style = ROOT.gStyle
        original_force = ROOT.gROOT.GetForceStyle()
        self.addCleanup(original_style.cd)
        style = ana_atlas_style.use_root_style()
        self.assertEqual(style.GetName(), "ana_atlas_style")
        self.assertEqual(ROOT.gROOT.GetForceStyle(), original_force)
        self.assertEqual(ROOT.addressof(ana_atlas_style.use_root_style()), ROOT.addressof(style))

        graph = ROOT.TGraphErrors(1)
        ROOT.ana_atlas_style.Signal(graph)
        graph.SetLineColor(ROOT.kMagenta)
        graph.SetLineStyle(1)
        graph.SetLineWidth(4)
        self.assertEqual(graph.GetLineColor(), ROOT.kMagenta)
        self.assertEqual(graph.GetLineStyle(), 1)
        self.assertEqual(graph.GetLineWidth(), 4)

    def test_python_and_root_color_roles_match(self):
        import ROOT

        original_style = ROOT.gStyle
        self.addCleanup(original_style.cd)
        ana_atlas_style.use_root_style()

        def rgb_hex(identifier):
            color = ROOT.gROOT.GetColor(identifier)
            channels = (color.GetRed(), color.GetGreen(), color.GetBlue())
            return "#" + "".join(f"{round(c * 255):02X}" for c in channels)

        for role, expected in ana_atlas_style.COLORS.items():
            actual = getattr(ROOT.ana_atlas_style.colors, role.title())()
            self.assertEqual(rgb_hex(actual), expected, role)
        for role, expected in ana_atlas_style.FILL_COLORS.items():
            actual = getattr(ROOT.ana_atlas_style.colors, role.title() + "Fill")()
            self.assertEqual(rgb_hex(actual), expected, role)
        for index, (accent, fill) in enumerate(zip(
            ana_atlas_style.SERIES_COLORS, ana_atlas_style.SERIES_FILL_COLORS
        )):
            self.assertEqual(rgb_hex(ROOT.ana_atlas_style.colors.Series(index)), accent)
            self.assertEqual(rgb_hex(ROOT.ana_atlas_style.colors.SeriesFill(index)), fill)
        histogram = ROOT.TH1D("background_palette", "", 1, 0, 1)
        histogram.SetDirectory(0)
        for index in range(len(ana_atlas_style.BACKGROUND_COLORS) + 1):
            ROOT.ana_atlas_style.Background(histogram, index)
            style = ana_atlas_style.artist_style("background", index=index)
            self.assertEqual(rgb_hex(histogram.GetLineColor()), style["edgecolor"])
            self.assertEqual(rgb_hex(histogram.GetFillColor()), style["facecolor"])


if __name__ == "__main__":
    unittest.main()
