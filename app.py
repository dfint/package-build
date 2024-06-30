import shutil
from pathlib import Path

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

        with st.status("Building package...", expanded=True) as status:
            root_dir = Path(__file__).parent
            build_dir = root_dir / "build"
            shutil.rmtree(build_dir)
            build_dir.mkdir(parents=True)

            package_name_no_extension = "dfint"
            package_path = root_dir / f"{package_name_no_extension}.zip"
            package_path.unlink(missing_ok=True)
            package_path_without_extension = root_dir / "dfint"

            (build_dir / hook_info.dfhooks_name).write_bytes(parts.dfhooks)

            lib_name = "dfhooks_dfint.dll" if operating_systems.startswith("win") else "libdfhooks_dfint.so"
            (build_dir / lib_name).write_bytes(parts.library)

            dfint_data_dir = build_dir / "dfint-data"
            dfint_data_dir.mkdir()

            (dfint_data_dir / "config.toml").write_bytes(parts.config)
            (dfint_data_dir / "offsets.toml").write_bytes(parts.offsets)

            (dfint_data_dir / "dictionary.csv").write_bytes(parts.csv_file)
            (dfint_data_dir / "encoding.toml").write_bytes(parts.encoding_config)

            art_dir = build_dir / "data" / "art"
            art_dir.mkdir(parents=True)
            (art_dir / "curses_640x300.png").write_bytes(parts.font_file)

            shutil.make_archive(
                package_name_no_extension,
                format="zip",
                base_dir=build_dir.relative_to(root_dir),
            )

            status.update(label="Package ready!", state="complete", expanded=False)

        st.download_button(
            label="Download package",
            file_name=package_path.name,
            data=package_path.read_bytes(),
            mime="application/zip",
        )
