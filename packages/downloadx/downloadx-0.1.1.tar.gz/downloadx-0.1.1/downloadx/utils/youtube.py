import os
from pathlib import Path
from downloadx.utils import Utils
from downloadx.helpers.strings import is_url
from downloadx._typed import YouTubeInfo, YouTubeStream
from pytube import YouTube as _Youtube
from alive_progress import alive_bar


class Youtube(Utils):
    _is_title: bool = True

    _instance: _Youtube
    _instance_info: YouTubeInfo

    def __init__(self, url: str, refactore_title: bool = True) -> None:
        super().__init__()

        self._is_title = refactore_title
        if u := is_url(url):
            self._instance = _Youtube(url=u)
            return self.verify()

        self.is_error(Exception(f"'{url}' is invalid URL"))

    def verify(self) -> None:
        try:
            self._instance.check_availability()
        except Exception as err:
            self.is_error(err)

    def download_audio(self, output: str = 'outputs') -> None:
        aud = self._instance \
            .streams \
            .filter(only_audio=True) \
            .first()

        if not aud:
            return self.is_error(Exception('content not found'))

        if not os.path.exists(Path(output)):
            os.makedirs(output, exist_ok=True)

        filename = f"{aud.title}.mp3" if not self._is_title else f"{aud.title.title()}.mp3"
        file_save = Path(output).joinpath(filename).as_posix()

        print(f"\033[F\033[K > {self._instance.watch_url}: {filename}")
        with alive_bar(round(aud.filesize_mb)) as bar:
            def on_prog(s, c, b) -> None:
                bar(len(c) / (1024 * 1024))

            self._instance.register_on_progress_callback(on_prog)
            aud.download(filename=file_save, skip_existing=True, max_retries=3)
            bar(aud.filesize_mb)

    def init_video(self) -> None:
        streams = self._instance \
            .streams \
            .filter(type='video', progressive=True)

        self._instance_info = YouTubeInfo(title=self._instance.title)
        for stream in streams:
            _stream = YouTubeStream(
                itag=stream.itag,
                resolution=f"{stream.resolution} {stream.mime_type.split('/')[1]}",
                str_size=f"{round(stream.filesize_mb, 1)} MB"
            )

            self._instance_info.streams.append(_stream)

    def download_video(self, stream: YouTubeStream, output: str = 'outputs') -> None:
        _stream = self._instance.streams.get_by_itag(stream.itag)
        if not _stream:
            raise Exception(f"No stream found with itag '{stream.itag}'")

        if not os.path.exists(Path(output)):
            os.makedirs(output, exist_ok=True)

        ext = _stream.mime_type.split('/')[1]
        filename = f"{_stream.title}.{ext}" if not self._is_title else f"{_stream.title.title()}.{ext}"
        file_save = Path(output).joinpath(filename).as_posix()

        print(f"\033[F\033[K > {self._instance.watch_url}: {filename}")
        with alive_bar(round(_stream.filesize_mb)) as bar:
            def on_prog(s, c, b) -> None:
                bar(len(c) / (1024 * 1024))

            self._instance.register_on_progress_callback(on_prog)
            _stream.download(filename=file_save, skip_existing=True, max_retries=3)
            bar(_stream.filesize_mb)