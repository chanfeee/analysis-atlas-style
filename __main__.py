"""Small discovery CLI; this module never imports a plotting backend."""

import argparse

from . import __version__, root_include_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description="Discover the ATLAS style package.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--root-include", action="store_true",
        help="print the directory containing AtlasStyle.h for C++ include paths",
    )
    args = parser.parse_args(argv)
    if args.root_include:
        print(root_include_dir())
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
