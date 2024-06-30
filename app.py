from pathlib import Path

import streamlit as st

from package_build.download_parts import download_parts
from package_build.metadata import get_dict_metadata, get_hook_metadata
from package_build.models import DictInfoEntry
from package_build.package import build_package
from package_build.parse_metadata import parse_metadata

hook_metadata = parse_metadata(get_hook_metadata())

dict_metadata = get_dict_metadata()

column1, column2 = st.columns(2)

df_version_options = hook_metadata.df_version_options

with column1:
    df_version: str = st.selectbox(label="DF version", options=sorted(df_version_options, reverse=True))
    operating_system: str = st.selectbox(
        label="Operating system/platform",
        options=df_version_options[df_version].operating_systems,
    )

with column2:
    df_variant: str = st.selectbox(label="DF variant", options=df_version_options[df_version].variants)
    dict_entry: DictInfoEntry = st.selectbox(label="Language", options=dict_metadata)

hook_info = hook_metadata.hook_info.get((df_version, df_variant, operating_system))

if not hook_info:
    st.write("Cannot create package for these parameters")
else:
    button_generate = st.button("Generate package")
    if button_generate:
        with st.status("Downloading files...", expanded=True) as status:
            parts = download_parts(hook_info, dict_entry)
            status.update(label="Download complete!", state="complete", expanded=False)

        with st.status("Building package...", expanded=True) as status:
            root_dir = Path(__file__).parent
            build_dir = root_dir / "build"
            package_name = f"dfint_{df_version}_{df_variant}_{operating_system}_{dict_entry.code}.zip"
            package_path = root_dir / package_name
            build_package(
                package_path=package_path,
                build_dir=build_dir,
                hook_info=hook_info,
                parts=parts,
                is_win=operating_system.startswith("win"),
            )
            status.update(label="Package ready!", state="complete", expanded=False)

        st.download_button(
            label="Download package",
            file_name=package_path.name,
            data=package_path.read_bytes(),
            mime="application/zip",
        )
