import streamlit as st
from .models import DictInfoEntry, HookInfoEntry
import requests


def download(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content


# @st.cache_data
def download_parts(hook_info: HookInfoEntry, dict_info: DictInfoEntry):
    library = download(hook_info.lib)
    config = download(hook_info.config)
    offsets = download(hook_info.offsets)
    csv_file = download(dict_info.csv)
    font_file = download(dict_info.font)
    encoding_config = download(dict_info.encoding)
    return library, config, offsets, csv_file, font_file, encoding_config
