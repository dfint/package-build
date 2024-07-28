import contextlib
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from package_build.download_parts import DownloadedParts
from package_build.models import HookInfoEntry


def zip_directory(directory: Path, filename: Path) -> None:
    with ZipFile(filename, "w", ZIP_DEFLATED) as archive:
        for entry in directory.rglob("*"):
            archive.write(entry, entry.relative_to(directory))


def build_package(
    *,
    package_path: Path,
    build_dir: Path,
    hook_info: HookInfoEntry,
    parts: DownloadedParts,
    is_win: bool,
) -> None:
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(build_dir)

    build_dir.mkdir(parents=True)

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

    zip_directory(build_dir, package_path)


def get_file_modification_datetime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def package_up_to_date(package_path: Path, lifetime: timedelta = timedelta(hours=12)) -> bool:
    """
    Check if the package is up to date: it exists and it was created not earlier then 12 hours ago.
    """

    if not package_path.exists():
        return False

    modification_datetime = get_file_modification_datetime(package_path)
    return (modification_datetime + lifetime) > datetime.now(tz=timezone.utc)


def remove_stale_packages(root_dir: Path) -> None:
    for package_path in root_dir.glob("*.zip"):
        if not package_up_to_date(package_path, lifetime=timedelta(hours=13)):
            package_path.unlink(missing_ok=True)
