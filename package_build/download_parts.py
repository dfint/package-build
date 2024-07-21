from typing import NamedTuple

import requests
import streamlit as st

from package_build.i18n import get_lang

from .models import DictInfoEntry, HookInfoEntry


def download(url: str) -> bytes:
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    return response.content


class DownloadedParts(NamedTuple):
    library: bytes
    dfhooks: bytes
    config: bytes
    offsets: bytes
    csv_file: bytes
    font_file: bytes
    encoding_config: bytes


# @st.cache_data
def download_parts(hook_info: HookInfoEntry, dict_info: DictInfoEntry) -> DownloadedParts:
    lang = get_lang()
    _ = lang.gettext

    st.write(_("Downloading library..."))
    library = download(hook_info.lib)

    st.write(_("Downloading dfhooks library..."))
    dfhooks = download(hook_info.dfhooks)

    st.write(_("Downloading config..."))
    config = download(hook_info.config)

    st.write(_("Downloading offsets..."))
    offsets = download(hook_info.offsets)

    st.write(_("Downloading csv dictionary..."))
    csv_file = download(dict_info.csv)

    st.write(_("Downloading font file..."))
    font_file = download(dict_info.font)

    st.write(_("Downloading encoding config..."))
    encoding_config = download(dict_info.encoding)

    return DownloadedParts(
        library=library,
        dfhooks=dfhooks,
        config=config,
        offsets=offsets,
        csv_file=csv_file,
        font_file=font_file,
        encoding_config=encoding_config,
    )
