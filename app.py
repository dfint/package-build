import streamlit as st

from package_build.download_parts import download_parts
from package_build.metadata import get_dict_metadata, get_hook_metadata
from package_build.models import DictInfoEntry
from package_build.parse_metadata import parse_metadata

hook_metadata = parse_metadata(get_hook_metadata())

dict_metadata = get_dict_metadata()

column1, column2 = st.columns(2)

df_version_options = hook_metadata.df_version_options

with column1:
    df_version: str = st.selectbox(label="DF version", options=sorted(df_version_options, reverse=True))
    operating_systems: str = st.selectbox(
        label="Operating system/platform",
        options=df_version_options[df_version].operating_systems,
    )

with column2:
    df_variant: str = st.selectbox(label="DF variant", options=df_version_options[df_version].variants)
    dict_entry: DictInfoEntry = st.selectbox(label="Language", options=dict_metadata)

hook_info = hook_metadata.hook_info.get((df_version, df_variant, operating_systems))

if not hook_info:
    st.write("Cannot create package for these parameters")
else:
    button_generate = st.button("Generate package")
    if button_generate:
        with st.status("Downloading files...", expanded=True) as status:
            parts = download_parts(hook_info, dict_entry)
            status.update(label="Download complete!", state="complete", expanded=False)
