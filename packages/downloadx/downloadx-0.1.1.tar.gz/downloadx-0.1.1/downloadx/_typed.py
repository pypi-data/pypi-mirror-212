from enum import Enum
from pydantic import BaseModel, Field, validator
from pytube.streams import Stream


class CLIMode(Enum):
    YOUTUBE = 'youtube'
    INSTAGRAM = 'instagram'

class MainCLI(BaseModel):
    mode: str

class YoutubeCLI(MainCLI):
    url: str | None
    url_file: str | None
    audio_only: bool
    output: str
    urls: list[str] = Field(default=[])

class InstagramCLI(MainCLI):
    url: str | None
    url_file: str | None

class YouTubeStream(BaseModel):
    itag: int
    str_size: str
    resolution: str

class YouTubeInfo(BaseModel):
    title: str
    streams: list[YouTubeStream] = Field(default=[])
