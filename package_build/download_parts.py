import streamlit as st
from .models import DictInfoEntry, HookInfoEntry
import requests


def download(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


# @st.cache_data
def download_parts(hook_info: HookInfoEntry, dict_info: DictInfoEntry):
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
    return library, config, offsets, csv_file, font_file, encoding_config
