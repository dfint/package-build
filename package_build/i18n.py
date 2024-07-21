import gettext as gettext_module
import re
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


def get_lang() -> gettext_module.NullTranslations:
    locale_dir = Path(__file__).parent / "locale"

    user_languages = get_preferred_languages()
    logger.info(f"User languages: {user_languages}")

    lang = gettext_module.translation(
        "messages",
        localedir=str(locale_dir),
        languages=user_languages,
        fallback=True,
    )

    lang.install()
    return lang


class LanguageWrapper:
    def __init__(self) -> None:
        pass

    def gettext(self, message: str) -> str:
        lang = get_lang()
        return lang.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        lang = get_lang()
        return lang.ngettext(singular, plural, n)


lang = LanguageWrapper()
gettext = lang.gettext
ngettext = lang.ngettext
