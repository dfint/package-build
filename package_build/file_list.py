from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from package_build.package import get_file_modification_datetime, package_up_to_date


def show_file_list(root_dir: Path) -> None:
    st.subheader("Package files awailable to download")

    if not list(root_dir.glob("*.zip")):
        st.write("No package files available.")
        return

    column1, column2, column3 = st.columns([3, 2, 1], vertical_alignment="center")
    column1.write("Package name")
    column2.write("When created")

    for package_path in sorted(root_dir.glob("*.zip")):
        if not package_up_to_date(package_path):
            continue

        column1, column2, column3 = st.columns([3, 2, 1], vertical_alignment="center")
        column1.write(package_path.relative_to(root_dir).name)
        hours_ago = (datetime.now(tz=timezone.utc) - get_file_modification_datetime(package_path)).seconds // 3600
        if hours_ago == 0:
            column2.write("less than an hour ago")
        else:
            column2.write(f"{hours_ago} hours ago")

        column3.download_button(
            label="Download",
            file_name=package_path.name,
            data=package_path.read_bytes(),
            mime="application/zip",
        )
