import re
from typing import NamedTuple

from .models import HookInfoEntry


class MetadataParsingResult(NamedTuple):
    df_versions: list[str]
    variants: list[str]
    operating_systems: list[str]
    mapping: dict[tuple[str, str, str], HookInfoEntry]


def parse_url(url: str) -> tuple[str, str, str]:
    result = re.search(r"offsets/([\w\.-]+)_([a-z]+)_([a-z\d]+)\.toml", url)
    if not result:
        msg = f"Cannot parse offsets URL: {url!r}"
        raise ValueError(msg)
    version, variant, os = result.groups()
    return version, variant, os


def parse_metadata(metadata: list[HookInfoEntry]) -> MetadataParsingResult:
    mapping = {}
    df_versions = set()
    variants = set()
    operating_systems = set()

    for item in metadata:
        version, variant, os = parse_url(item.offsets)
        mapping[(version, variant, os)] = item
        df_versions.add(version)
        variants.add(variant)
        operating_systems.add(os)

    return MetadataParsingResult(
        sorted(df_versions, reverse=True),
        sorted(variants),
        sorted(operating_systems),
        mapping,
    )
