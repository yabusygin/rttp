from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional


def _parse_args(args: Optional[List[str]] = None) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--role-path", type=Path, default=Path("."))
    return parser.parse_args(args)
