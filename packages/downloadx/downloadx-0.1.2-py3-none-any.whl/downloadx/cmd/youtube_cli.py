import argparse

from downloadx._typed import YoutubeCLI as _YoutubeCLI
from downloadx.cmd import Command as _Coomand
from downloadx.helpers.strings import is_url
from downloadx.utils.youtube import Youtube


class YoutubeCLI(_Coomand):
    _parser: argparse.ArgumentParser

    def __init__(
        self, parser: argparse.ArgumentParser, sp: argparse.ArgumentParser
    ) -> None:
        super().__init__()

        self._parser = parser
        sp.add_argument(
            "-u", "--url", type=str, help="single url download", dest="url", metavar=""
        )
        sp.add_argument(
            "-f",
            "--url-file",
            type=str,
            help="multiple url download by defining url inside a file",
            metavar="",
        )
        sp.add_argument(
            "-o",
            "--output",
            help="folder to save downloaded files. default is './outputs' directory",
            default="outputs",
            metavar="",
        )
        sp.add_argument(
            "--audio-only", help="download audio only (.mp3)", action="store_true"
        )

        parser.parse_args(["youtube"])

    def exec(self) -> None:
        args = self._optimize_args()

        urls = [f"\n> {i}" for i in args.urls]
        if self.confirm(f'\nURL of the content to be downloaded:{"".join(urls)}'):
            queues: list[dict] = []
            for url in args.urls:
                yt = Youtube(url)

                if args.audio_only:
                    yt.download_audio(args.output)
                    continue

                yt.init_video()
                choices: list[str] = []
                for i, stream in enumerate(yt._instance_info.streams):
                    choices.append(
                        f"\n   {i + 1}. \u0009{stream.resolution} - {stream.str_size}"
                    )

                _range = len(choices)
                if _range > 1:
                    _range = f"1 - {_range}"

                idx = 0
                while True:
                    try:
                        self.clear()
                        idx = int(
                            input(
                                f"\nplease select the resolution to download for '{yt._instance_info.title}': {''.join(choices)} \n\n[{_range}]: "
                            )
                        )
                        if idx >= 1 and idx <= len(choices):
                            idx -= 1
                            break
                    except Exception:
                        pass

                queues.append(
                    {"func": yt.download_video, "arg": yt._instance_info.streams[idx]}
                )

            if queues:
                self.clear()
                for queue in queues:
                    queue["func"](queue["arg"], args.output)

            self.ok()

    def _optimize_args(self) -> _YoutubeCLI:
        args = _YoutubeCLI(**self._parser.parse_args().__dict__)

        if not args.url and not args.url_file:
            self.abort(
                "there is no content to download. you need to provide a value in the --url or --url-file argument"
            )

        args.urls = []
        if url := is_url(args.url or ""):
            args.urls.append(url)
        elif args.url is not None and args.url != "":
            self.abort(f"'{args.url}' is not valid YouTube url")

        if file := args.url_file:
            try:
                with open(file, "r") as f:
                    contents = [
                        i.strip() for i in f.read().split("\n") if i.strip() != ""
                    ]
                    for url in contents:
                        if u := is_url(url):
                            args.urls.append(u)
                            continue

                        self.abort(f"'{url}' is not valid YouTube url")
            except Exception as err:
                self.abort(str(err))

        return args
