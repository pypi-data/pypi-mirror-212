from urllib.parse import urlparse


def is_url(url: str) -> str | None:
    if u := url.strip():
        parsed_url = urlparse(u)
        if all([parsed_url.scheme, parsed_url.netloc]):
            return u