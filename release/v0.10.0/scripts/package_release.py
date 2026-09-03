#!/usr/bin/env python3
"""Write the release manifest and a deterministic external ZIP."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 8, 18, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_files() -> list[Path]:
    excluded_parts = {"__pycache__", ".git", ".pytest_cache"}
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "MANIFEST.sha256":
            continue
        if any(part in excluded_parts for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in {".pyc", ".tmp"} or path.name.endswith("~"):
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def write_manifest(files: list[Path]) -> Path:
    manifest = ROOT / "MANIFEST.sha256"
    lines = [f"{sha256(path)}  ./{path.relative_to(ROOT).as_posix()}" for path in files]
    temporary = manifest.with_suffix(".sha256.tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.replace(temporary, manifest)
    return manifest


def write_zip(output: Path, files: list[Path], manifest: Path) -> None:
    try:
        output.resolve().relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise SystemExit("El ZIP debe escribirse fuera de la raíz del release")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    root_name = ROOT.name
    members = sorted(files + [manifest], key=lambda p: p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in members:
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"{root_name}/{rel}", date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if path.suffix == ".py" else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    os.replace(temporary, output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    files = release_files()
    manifest = write_manifest(files)
    write_zip(args.output.resolve(), files, manifest)
    print(f"manifest_entries={len(files)}")
    print(f"physical_files={len(files) + 1}")
    print(f"zip={args.output.resolve()}")
    print(f"zip_sha256={sha256(args.output.resolve())}")


if __name__ == "__main__":
    main()
