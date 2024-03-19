import re
from typing import NamedTuple
from .models import HookInfoEntry


class MetadataParsingResult(NamedTuple):
    df_versions: list[str]
    variants: list[str]
    operating_systems: list[str]
    mapping: dict[tuple[str, str, str], HookInfoEntry]


def parse_url(url: str) -> tuple[str, str, str]:
    version, variant, os = re.search(r"offsets/([\d\.]+)_([a-z]+)_([a-z\d]+)\.toml", url).groups()
    return version, variant, os


def parse_metadata(metadata: list[HookInfoEntry]) -> MetadataParsingResult:
    mapping = dict()
    df_versions = set()
    variants = set()
    operating_systems = set()

    for item in metadata:
        version, variant, os = parse_url(item.offsets)
        mapping[(version, variant, os)] = item
        df_versions.add(version)
        variants.add(variant)
        operating_systems.add(os)

    return MetadataParsingResult(sorted(df_versions), sorted(variants), sorted(operating_systems), mapping)
