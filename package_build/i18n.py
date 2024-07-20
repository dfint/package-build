import gettext
from pathlib import Path

locale_dir = Path(__file__).parent / "locale"

locale = "ru"
lang = gettext.translation(
    "messages",
    localedir=str(locale_dir),
    languages=[locale],
    fallback=True,
)

lang.install()
_ = lang.gettext
ngettext = lang.ngettext
