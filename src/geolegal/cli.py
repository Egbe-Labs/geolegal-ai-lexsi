"""Dependency-free command-line entry point for local verification."""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version


def package_version() -> str:
    """Return installed metadata version, or the source-tree version."""
    try:
        return version("geolegal-ai")
    except PackageNotFoundError:
        from geolegal import __version__

        return __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="geolegal",
        description="GeoLegal-AI research pipeline (not legal advice)",
    )
    parser.add_argument("--version", action="version", version=package_version())
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
