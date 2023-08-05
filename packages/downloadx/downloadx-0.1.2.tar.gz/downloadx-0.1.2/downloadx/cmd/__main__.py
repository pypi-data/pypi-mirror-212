import argparse

from downloadx._typed import CLIMode, MainCLI
from downloadx.cmd import Command as _Command
from downloadx.cmd.instagram_cli import InstagramCLI
from downloadx.cmd.youtube_cli import YoutubeCLI
from downloadx.helpers import enums


class Command(_Command):
    def __init__(self) -> None:
        super().__init__()

        parser = argparse.ArgumentParser(description="DownloadX CLI")
        subparser = parser.add_subparsers(title="DownloadX CLI Mode", dest="mode")

        youtube_cli = YoutubeCLI(
            parser, subparser.add_parser("youtube", help="YouTube CLI")
        )
        instagram_cli = InstagramCLI(
            parser, subparser.add_parser("instagram", help="Instagram CLI")
        )

        switcher = {
            CLIMode.YOUTUBE.value: youtube_cli,
            CLIMode.INSTAGRAM.value: instagram_cli,
        }

        args = MainCLI(**parser.parse_args().__dict__)

        if mode := enums.from_str(CLIMode, args.mode):
            if func := switcher.get(mode.value):
                return func.exec()
