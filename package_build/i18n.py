import gettext
import time
from functools import cache
from pathlib import Path

from streamlit_javascript import st_javascript


@cache
def get_preferred_languages() -> list[str]:
    while True:
        languages = st_javascript("navigator.languages")
        if languages:
            return languages

        time.sleep(0.1)


locale_dir = Path(__file__).parent / "locale"

languages = get_preferred_languages()
lang = gettext.translation(
    "messages",
    localedir=str(locale_dir),
    languages=languages,
    fallback=True,
)

lang.install()
_ = lang.gettext
ngettext = lang.ngettext
