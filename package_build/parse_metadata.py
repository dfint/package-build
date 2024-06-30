import re
from dataclasses import dataclass, field
from typing import NamedTuple

from .models import HookInfoEntry


@dataclass
class DFVersionOptions:
    variants: set[str] = field(default_factory=set)
    operating_systems: set[str] = field(default_factory=set)


class MetadataParsingResult(NamedTuple):
    df_version_options: dict[str, DFVersionOptions]
    hook_info: dict[tuple[str, str, str], HookInfoEntry]


def parse_url(url: str) -> tuple[str, str, str]:
    result = re.search(r"offsets/([\w\.-]+)_([a-z]+)_([a-z\d]+)\.toml", url)
    if not result:
        msg = f"Cannot parse offsets URL: {url!r}"
        raise ValueError(msg)
    version, variant, os = result.groups()
    return version, variant, os


def parse_metadata(metadata: list[HookInfoEntry]) -> MetadataParsingResult:
    version_to_metadata_mapping: dict[str, DFVersionOptions] = {}
    hook_info = {}

    for item in metadata:
        version, variant, os = parse_url(item.offsets)
        hook_info[(version, variant, os)] = item
        df_version_info = version_to_metadata_mapping.get(version, DFVersionOptions())
        df_version_info.variants.add(variant)
        df_version_info.operating_systems.add(os)
        version_to_metadata_mapping[version] = df_version_info

    return MetadataParsingResult(
        version_to_metadata_mapping,
        hook_info,
    )
