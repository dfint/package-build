import gettext

gettext.bindtextdomain("messages", "locales")
gettext.textdomain("messages")

locale = "en"
lang = gettext.translation("messages", localedir="locales", languages=[locale])

lang.install()
_ = lang.gettext
ngettext = lang.ngettext
