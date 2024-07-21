from datetime import timedelta

import requests
import streamlit as st

from package_build.i18n import gettext as _

from .models import DictInfoEntry, HookInfoEntry


def get_json(url: str) -> list[dict]:
    response = requests.get(url, timeout=300)
    response.raise_for_status()
    return response.json()


metadata_url_base = "https://dfint.github.io/update-data/metadata/"
dict_metadata_url = metadata_url_base + "dict.json"
hook_metadata_url = metadata_url_base + "hook_v2.json"


@st.cache_data(show_spinner=_("Getting hook metadata..."), ttl=timedelta(minutes=15))
def get_hook_metadata() -> list[HookInfoEntry]:
    data = get_json(hook_metadata_url)
    return [HookInfoEntry.model_validate(item) for item in data]


@st.cache_data(show_spinner=_("Getting dict metadata..."), ttl=timedelta(minutes=15))
def get_dict_metadata() -> list[DictInfoEntry]:
    data = get_json(dict_metadata_url)
    return [DictInfoEntry.model_validate(item) for item in data if item.get("code")]
