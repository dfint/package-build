import gettext as gettext_module
import re
from functools import lru_cache
from pathlib import Path

from loguru import logger
from streamlit.web.server.websocket_headers import _get_websocket_headers


def get_preferred_languages() -> list[str]:
    try:
        headers = _get_websocket_headers() or {}
    except RuntimeError:
        headers = {}

    accept_language = headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


@lru_cache(maxsize=128, typed=False)
def get_lang(languages: tuple[str]) -> gettext_module.NullTranslations:
    logger.info(f"Languages: {languages}")
    locale_dir = Path(__file__).parent / "locale"

    return gettext_module.translation(
        "messages",
        localedir=locale_dir,
        languages=languages,
        fallback=True,
    )



class LanguageWrapper:
    def __init__(self) -> None:
        pass

    def gettext(self, message: str) -> str:
        lang = get_lang(tuple(get_preferred_languages()))
        return lang.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        lang = get_lang(tuple(get_preferred_languages()))
        return lang.ngettext(singular, plural, n)


lang = LanguageWrapper()
gettext = lang.gettext
ngettext = lang.ngettext
