import streamlit as st

from package_build.download_parts import download_parts
from package_build.metadata import get_dict_metadata, get_hook_metadata
from package_build.models import DictInfoEntry
from package_build.parse_metadata import parse_metadata

hook_metadata = parse_metadata(get_hook_metadata())

dict_metadata = get_dict_metadata()

column1, column2 = st.columns(2)

with column1:
    df_version: str = st.selectbox(label="DF version", options=hook_metadata.df_versions)
    operating_systems: str = st.selectbox(label="Operating system/platform", options=hook_metadata.operating_systems)

with column2:
    df_variant: str = st.selectbox(label="DF variant", options=hook_metadata.variants)
    dict_entry: DictInfoEntry = st.selectbox(label="Language", options=dict_metadata)

hook_info = hook_metadata.mapping.get((df_version, df_variant, operating_systems))

if not hook_info:
    st.write("Cannot create package for these parameters")
else:
    button_generate = st.button("Generate package")
    if button_generate:
        with st.status("Downloading files...", expanded=True) as status:
            parts = download_parts(hook_info, dict_entry)
            status.update(label="Download complete!", state="complete", expanded=False)
