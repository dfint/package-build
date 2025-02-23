from pathlib import Path

import streamlit as st
from streamlit_gettext import get_preferred_languages

from package_build.download_parts import download_parts
from package_build.file_list import show_file_list
from package_build.i18n import gettext as _
from package_build.metadata import get_dict_metadata, get_hook_metadata
from package_build.models import DictInfoEntry
from package_build.package import build_package, package_up_to_date, remove_stale_packages
from package_build.parse_metadata import parse_metadata

st.set_page_config(page_title=_("DF localization package builder"), page_icon="📦")

st.header(_("DF localization package builder"))
st.write(_("Build/download a package, unpack into the game's directory with file repalacement."))
st.markdown(
    _(
        "It's recommended to use [dfint-installer](https://github.com/dfint/installer) instead of using this "
        "app. Use the package builder only if the installer doesn't work for you or you have some other issues "
        "with it.",
    ),
)

hook_metadata = parse_metadata(get_hook_metadata())
dict_metadata = get_dict_metadata()
df_version_options = hook_metadata.df_version_options

column1, column2 = st.columns(2)
with column1:
    df_version: str = st.selectbox(label=_("DF version"), options=sorted(df_version_options, reverse=True))
    operating_system: str = st.selectbox(
        label=_("Operating system/platform"),
        options=sorted(df_version_options[df_version].operating_systems, reverse=True),  # show windows first
    )

variants_priority = {
    "steam": 0,
    "itchio": 1,
    "classic": 2,
}

variants = sorted(df_version_options[df_version].variants, key=lambda v: variants_priority.get(v, 3))


def language_ordering(dict_info_entry: DictInfoEntry) -> tuple[int, str]:
    """
    Set max priority to user's languages (according to their index in the user's browser settings)
    and the lowest priority to English.

    All other languages are sorted by their codes.
    """
    user_languages = get_preferred_languages()

    def get_language_priority(language_code: str) -> int:
        if language_code.startswith("en"):
            return 1000

        try:
            return user_languages.index(dict_info_entry.code) - len(user_languages)
        except ValueError:
            return 0

    return (get_language_priority(dict_info_entry.code), dict_info_entry.code)



with column2:
    df_variant: str = st.selectbox(label=_("DF variant"), options=variants)
    dict_entry: DictInfoEntry = st.selectbox(label=_("Language"), options=sorted(dict_metadata, key=language_ordering))

hook_info = hook_metadata.hook_info.get((df_version, df_variant, operating_system))

root_dir = Path(__file__).parent

with st.spinner(_("Removing stale packages...")):
    remove_stale_packages(root_dir)

if not hook_info:
    st.write(_("Cannot create package with these parameters"))
else:
    package_name = f"dfint_{df_version}_{df_variant}_{operating_system}_{dict_entry.code}.zip"
    package_path = root_dir / package_name

    if not package_up_to_date(package_path):
        button_generate = st.button(_("Generate package"))
        if button_generate:
            with st.status(_("Downloading files..."), expanded=True) as status:
                parts = download_parts(hook_info, dict_entry)
                status.update(label=_("Downloading complete!"), state="complete", expanded=False)

            with st.status(_("Building package..."), expanded=True) as status:
                build_dir = root_dir / "build"

                build_package(
                    package_path=package_path,
                    build_dir=build_dir,
                    hook_info=hook_info,
                    parts=parts,
                    is_win=operating_system.startswith("win"),
                )
                status.update(label=_("Package is ready!"), state="complete", expanded=False)

    if package_up_to_date(package_path):
        st.download_button(
            label=_("Download package"),
            file_name=package_path.name,
            data=package_path.read_bytes(),
            mime="application/zip",
        )

enable_filter = st.checkbox(label=_("Filter available files by DF variant, operating system, language"), value=True)
glob_filter = f"*_{df_variant}_{operating_system}_{dict_entry.code}.zip" if enable_filter else "*.zip"


def file_sort_key(file_path: Path) -> tuple[str, str, str, str]:
    _, version, variant, os, language = file_path.name.split("_")
    return (
        language,
        os,
        variant,
        version,
    )


show_file_list(root_dir, glob_filter=glob_filter, sort_key=file_sort_key)
