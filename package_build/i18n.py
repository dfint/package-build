import gettext
import time
from pathlib import Path

import streamlit as st
from streamlit_javascript import st_javascript


def get_preferred_languages() -> list[str]:
    with st.empty():
        while True:
            languages = st_javascript("window.navigator.languages")

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
