import shutil
from pathlib import Path

from package_build.download_parts import DownloadedParts
from package_build.models import HookInfoEntry


def build_package(
    *,
    root_dir: Path,
    build_dir: Path,
    hook_info: HookInfoEntry,
    parts: DownloadedParts,
    is_win: bool,
) -> Path:
    shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    package_name_no_extension = "dfint"
    package_path = root_dir / f"{package_name_no_extension}.zip"
    package_path.unlink(missing_ok=True)

    (build_dir / hook_info.dfhooks_name).write_bytes(parts.dfhooks)

    lib_name = "dfhooks_dfint.dll" if is_win else "libdfhooks_dfint.so"
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

    return package_path
