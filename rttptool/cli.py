from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional

from .discovery import discover_tests
from .exception import AssertError, TestDefinitionError
from .test import Test


def _parse_args(args: Optional[List[str]] = None) -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--role-path", type=Path, default=Path("."))
    return parser.parse_args(args)


def main(argv: Optional[List[str]] = None) -> None:
    args = _parse_args(argv)
    tests_path = Path(args.role_path, "templates_tests")
    if tests_path.is_dir():
        try:
            for testdef, src_path in discover_tests(tests_path):
                test = Test(args.role_path, src_path, testdef)
                print("[{}] {} ... ".format(src_path, testdef.name), end="")
                try:
                    test.run()
                except AssertError as exc:
                    print("fail")
                    print(exc.args[0])
                    break
                else:
                    print("ok")
        except TestDefinitionError as exc:
            exception: Optional[BaseException] = exc
            print("TestDefinitionError", end="")
            while exception is not None:
                print(": {}".format(exception.args[0]), end="")
                exception = exception.__cause__
