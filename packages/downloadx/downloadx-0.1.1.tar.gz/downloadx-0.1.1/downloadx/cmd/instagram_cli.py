import argparse
from downloadx.cmd import Command as _Coomand
from downloadx._typed import InstagramCLI as _InstagramCLI


class InstagramCLI(_Coomand):
    _parser: argparse.ArgumentParser

    def __init__(self, parser: argparse.ArgumentParser, sp: argparse.ArgumentParser) -> None:
        super().__init__()

        self._parser = parser
        sp.add_argument("--url", type=str, help="single Instagram url download")
        sp.add_argument("--url-file", type=str, help="multiple Instagram url download with txt file input")

        parser.parse_args(['instagram'])

    def exec(self) -> None:
        args = _InstagramCLI(**self._parser.parse_args().__dict__)
        print(args)
        """"""