from __future__ import annotations

import unittest

from geolegal import __version__
from geolegal.cli import build_parser, main


class SmokeTests(unittest.TestCase):
    def test_package_version_is_declared(self) -> None:
        self.assertEqual(__version__, "0.1.0")

    def test_cli_parses_empty_arguments(self) -> None:
        self.assertEqual(main([]), 0)
        self.assertEqual(build_parser().prog, "geolegal")


if __name__ == "__main__":
    unittest.main()
