from typing import NamedTuple

import requests
import streamlit as st

from .models import DictInfoEntry, HookInfoEntry


def download(url: str) -> bytes:
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    return response.content


class DownloadedParts(NamedTuple):
    library: bytes
    config: bytes
    offsets: bytes
    csv_file: bytes
    font_file: bytes
    encoding_config: bytes


# @st.cache_data
def download_parts(
    hook_info: HookInfoEntry,
    dict_info: DictInfoEntry,
) -> tuple[bytes, bytes, bytes, bytes, bytes, bytes]:
    st.write("Download library...")
    library = download(hook_info.lib)

    st.write("Download config...")
    config = download(hook_info.config)

    st.write("Download offseets...")
    offsets = download(hook_info.offsets)

    st.write("Download csv dictionary...")
    csv_file = download(dict_info.csv)

    st.write("Download font file...")
    font_file = download(dict_info.font)

    st.write("Download encoding config...")
    encoding_config = download(dict_info.encoding)

    return DownloadedParts(
        library=library,
        config=config,
        offsets=offsets,
        csv_file=csv_file,
        font_file=font_file,
        encoding_config=encoding_config,
    )
