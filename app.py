import streamlit as st
from package_build.metadata import get_hook_metadata, get_dict_metadata
from package_build.models import DictInfoEntry

hook_metadata = get_hook_metadata()

dict_metadata = get_dict_metadata()

selected_dict_entry: DictInfoEntry = st.selectbox(label="Choose language", options=dict_metadata)
