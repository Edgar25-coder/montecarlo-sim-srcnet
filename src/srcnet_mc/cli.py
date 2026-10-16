"""Command-line entry points for validated development increments."""

from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="srcnet-mc")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("probe-scip", help="run the exact binary/nonlinear SCIP compatibility probe")
    arguments = parser.parse_args(argv)

    if arguments.command == "probe-scip":
        try:
            from srcnet_mc.optimization.scip_probe import run_probe

            result = run_probe()
        except ImportError as error:
            print(f"SCIP probe unavailable: {error}", file=sys.stderr)
            return 2
        print(json.dumps(result.to_dict(), sort_keys=True))
        return 0 if result.has_solution and result.status == "optimal" else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

