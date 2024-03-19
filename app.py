import streamlit as st
from package_build.metadata import get_hook_metadata, get_dict_metadata
from package_build.models import DictInfoEntry
from package_build.parse_metadata import parse_metadata
from rich import print

hook_metadata = parse_metadata(get_hook_metadata())
print(hook_metadata)

dict_metadata = get_dict_metadata()

selected_dict_entry: DictInfoEntry = st.selectbox(label="Choose language", options=dict_metadata)
