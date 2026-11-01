import logging
import random
import re
import string
import sys
import time
from typing import Dict, Optional

import requests

log = logging.getLogger()

# Recent stable Chrome releases (https://chromiumdash.appspot.com/releases).
# Only Windows/Linux: curl_cffi's default "chrome" TLS fingerprint is the
# desktop one, macOS Chrome has a slightly different fingerprint.
CHROME_PROFILES = (
    (156, "Windows"),
    (156, "Linux"),
    (155, "Windows"),
)

_UA_PLATFORMS = {
    "Windows": "Windows NT 10.0; Win64; x64",
    "Linux": "X11; Linux x86_64",
}


def _sec_ch_ua(major: int) -> str:
    """Brand list Chrome sends in sec-ch-ua, including the GREASE brand.

    Mirrors GetUserAgentBrandList in Chromium's
    components/embedder_support/user_agent_utils.cc, which derives the fake
    brand and the ordering from the major version.
    """
    chars = (" ", "(", ":", "-", ".", "/", ")", ";", "=", "?", "_")
    versions = ("8", "99", "24")
    orders = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))

    grease = f"Not{chars[major % 11]}A{chars[(major + 1) % 11]}Brand"
    brands = (
        (grease, versions[major % 3]),
        ("Chromium", str(major)),
        ("Google Chrome", str(major)),
    )
    ordered = [None] * 3
    for brand, position in zip(brands, orders[major % 6]):
        ordered[position] = brand
    return ", ".join(f'"{name}";v="{version}"' for name, version in ordered)


def random_browser_headers() -> Dict[str, str]:
    """Headers of a randomly picked recent desktop Chrome."""
    major, platform = random.choice(CHROME_PROFILES)
    return {
        "User-Agent": (
            f"Mozilla/5.0 ({_UA_PLATFORMS[platform]}) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36"
        ),
        "sec-ch-ua": _sec_ch_ua(major),
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": f'"{platform}"',
    }


class CustomSession(requests.Session):
    def __init__(
        self,
        max_retries: int = 3,
        min_backoff: int = 4,
        timeout: int = 10,
    ) -> None:
        super().__init__()
        self.max_retries = max_retries
        self.min_backoff = min_backoff
        self.timeout = timeout

    def request(self, method: str | bytes, url: str | bytes, **kwargs: ...) -> ...:  # pyright: ignore[reportIncompatibleMethodOverride]
        kwargs.setdefault("timeout", self.timeout)
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = super().request(method, url, **kwargs)
            except requests.RequestException as exc:
                last_exception = exc
                if attempt == self.max_retries:
                    raise

                time.sleep(self.min_backoff * (2**attempt))
                continue

            if response.status_code != 429 and response.status_code < 500:
                return response

            if attempt == self.max_retries:
                return response

            response.close()
            sleep_time = self.min_backoff * (2**attempt)
            log.info(f"Received status code: {response.status_code}, sleeping for {sleep_time}s")
            time.sleep(sleep_time)

        if last_exception is not None:
            raise last_exception
        raise RuntimeError("unreachable")


def is_oneshot(chapter_name: str, chapter_subtitle: str) -> bool:
    chapter_number = chapter_name_to_int(chapter_name)

    if chapter_number is not None:
        return False

    for name in (chapter_name, chapter_subtitle):
        name = name.lower()
        if "one" in name and "shot" in name:
            return True
    return False


def chapter_name_to_int(name: str) -> Optional[int]:
    try:
        return int(name.lstrip("#"))
    except ValueError:
        return None


def escape_path(path: str) -> str:
    return re.sub(r"[^\w]+", " ", path).strip(string.punctuation + " ")


def is_windows() -> bool:
    return sys.platform == "win32"
