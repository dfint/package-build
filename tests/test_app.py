from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from package_build.i18n import set_preferred_languages
from package_build.models import DictInfoEntry, HookInfoEntry

if TYPE_CHECKING:
    from collections.abc import Iterator

project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def apptest() -> Iterator[AppTest]:
    with (
        patch("package_build.metadata.get_hook_metadata") as get_hook_metadata,
        patch("package_build.metadata.get_dict_metadata") as get_dict_metadata,
    ):
        get_hook_metadata.return_value = [
            HookInfoEntry(
                df=0,
                checksum=0,
                lib="https://example.com/hook_0.1.0.dll",
                config="https://example.com/hook_0.1.0.dll",
                offsets="https://example.com/offsets/50.10_classic_win64.toml",
                dfhooks="https://example.com/dfhooks.dll",
            ),
        ]

        get_dict_metadata.return_value = [
            DictInfoEntry(
                language="English",
                code="en",
                csv="https://example.com/en.csv",
                font="https://example.com/cp437.png",
                encoding="https://example.com/cp437.toml",
                checksum=0,
            ),
            DictInfoEntry(
                language="Belarusian",
                code="be",
                csv="https://example.com/be.csv",
                font="https://example.com/cp437.png",
                encoding="https://example.com/cp437.toml",
                checksum=0,
            ),
            DictInfoEntry(
                language="Portuguese (Brazil)",
                code="pt_BR",
                csv="https://example.com/pt_BR.csv",
                font="https://example.com/cp437.png",
                encoding="https://example.com/cp437.toml",
                checksum=0,
            ),
        ]

        app_path = project_root / "app.py"
        yield AppTest.from_file(app_path).run()


def test_smoketest(apptest: AppTest):
    assert not apptest.exception, apptest.exception[0].stack_trace


def test_language_selector(apptest: AppTest):
    language_selector = apptest.segmented_control[0]
    assert "ru" in language_selector.options

    try:
        language_selector.set_value("ru").run()
        assert not apptest.exception, apptest.exception[0].stack_trace
        assert apptest.header[0].value == "Сборщик пакетов локализации для DF"
    finally:
        set_preferred_languages(None)


def test_brazilian_portuguese_is_prioritized(apptest: AppTest):
    try:
        apptest.segmented_control[0].set_value("pt_BR").run()
        language_selector = apptest.selectbox[-1]
        assert language_selector.value.code == "pt_BR"
    finally:
        set_preferred_languages(None)
