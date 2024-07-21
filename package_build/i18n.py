import gettext
import re
from pathlib import Path

from loguru import logger
from streamlit.web.server.websocket_headers import _get_websocket_headers


def get_preferred_languages() -> list[str]:
    headers = _get_websocket_headers() or {}
    accept_language = headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


locale_dir = Path(__file__).parent / "locale"

user_languages = get_preferred_languages()
logger.info(f"User languages: {user_languages}")

lang = gettext.translation(
    "messages",
    localedir=str(locale_dir),
    languages=user_languages,
    fallback=True,
)

lang.install()
_ = lang.gettext
ngettext = lang.ngettext
