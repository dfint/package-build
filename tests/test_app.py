from collections.abc import Callable
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from package_build.models import DictInfoEntry, HookInfoEntry


@pytest.fixture()
@patch("package_build.metadata.get_hook_metadata")
@patch("package_build.metadata.get_dict_metadata")
def apptest(get_dict_metadata: Callable, get_hook_metadata: Callable) -> AppTest:
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
    ]

    return AppTest.from_file("app.py").run()


def test_smoketest(apptest: AppTest):
    assert not apptest.exception, apptest.exception[0].stack_trace
