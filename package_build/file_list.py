from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from package_build.i18n import _, ngettext
from package_build.package import get_file_modification_datetime, package_up_to_date


def show_file_list(root_dir: Path) -> None:
    st.subheader(_("Package files awailable to download"))

    file_list = [file for file in root_dir.glob("*.zip") if package_up_to_date(file)]

    if not file_list:
        st.write(_("No package files available."))
        return

    column1, column2, column3 = st.columns([3, 2, 1], vertical_alignment="center")
    column1.write(_("Package name"))
    column2.write(_("When created"))

    for package_path in sorted(file_list):
        column1, column2, column3 = st.columns([3, 2, 1], vertical_alignment="center")
        column1.write(package_path.relative_to(root_dir).name)
        hours_ago = (datetime.now(tz=timezone.utc) - get_file_modification_datetime(package_path)).seconds // 3600
        if hours_ago == 0:
            column2.write(_("less than an hour ago"))
        else:
            column2.write(ngettext("%(num)d hour ago", "%(num)d hours ago", hours_ago) % {"num": hours_ago})

        column3.download_button(
            label=_("Download"),
            file_name=package_path.name,
            data=package_path.read_bytes(),
            mime="application/zip",
        )
