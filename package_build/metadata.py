import datetime

import requests
import streamlit as st

from .models import HookInfoEntry, DictInfoEntry


def get_json(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


metadata_url_base = "https://dfint.github.io/update-data/metadata/"
dict_metadata_url = metadata_url_base + "dict.json"
hook_metadata_url = metadata_url_base + "hook.json"


@st.cache_data(show_spinner="Getting hook metadata...", ttl=datetime.timedelta(minutes=15))
def get_hook_metadata() -> dict[int, HookInfoEntry]:
    data = get_json(hook_metadata_url)
    return {item["df"]: HookInfoEntry.model_validate(item) for item in data}


@st.cache_data(show_spinner="Getting dict metadata...", ttl=datetime.timedelta(minutes=15))
def get_dict_metadata() -> list[DictInfoEntry]:
    data = get_json(dict_metadata_url)
    return [DictInfoEntry.model_validate(item) for item in data]
