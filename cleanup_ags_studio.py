#!/usr/bin/env python3
import argparse, os, shutil, sys
from datetime import datetime
from pathlib import Path
VAULT_FOLDER = "AGS-VAULT"
BACKUP_PATTERNS = [".backup.py", "_backup.py", ".bak", ".old"]
PACK_PATTERN = ".pack"
ARCHIVE_PREFIXES = ["_archive_", "_pending_", "_old_", "_deprecated_"]
FULL_BACKUP_FOLDERS = ["enterprise_builder_backup_final6", "enterprise_builder_backup"]
PROTECTED = {".git", ".venv", "venv", "env", ".pytest_cache", "__pycache__", "node_modules"}
def log(m, l="INFO"):
    print(f"[{l}] {m}")
def is_protected(p):
    return any(x in p.parts for x in PROTECTED)
def is_backup_file(fn):
    return any(fn.endswith(p) for p in BACKUP_PATTERNS) or (PACK_PATTERN in fn and fn.endswith(".py"))
def is_archive_folder(dn):
    return any(dn.startswith(p) for p in ARCHIVE_PREFIXES)
def is_full_backup(dn):
    return dn in FULL_BACKUP_FOLDERS
def find_backups(root):
    found = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in PROTECTED]
        for f in fns:
            if is_backup_file(f):
                found.append(Path(dp) / f)
    return found
def find_archives(root):
    found = []
    for dp, dns, _ in os.walk(root):
        dns[:] = [d for d in dns if d not in PROTECTED]
        for d in dns:
            if is_archive_folder(d):
                found.append(Path(dp) / d)
    return found
def find_full_backups(root):
    return [p for p in root.iterdir() if p.is_dir() and is_full_backup(p.name)]
def move(src, dst, dry):
    if not src.exists():
        log(f"غير موجود: {src}", "ERR")
        return False
    if dst.exists():
        i = 1
        while dst.exists():
            dst = dst.parent / f"{dst.stem}__{i}{dst.suffix}"
            i += 1
    if dry:
        log(f"[DRY] {src.name} -> {dst}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        log(f"نقل: {src.name} -> {dst}", "MOVE")
    return True
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    dry = not args.execute
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    vault = root / VAULT_FOLDER / ("backups" if dry else f"backups/{ts}")
    archive = root / VAULT_FOLDER / ("archive" if dry else f"archive/{ts}")
    log(f"=== {'DRY-RUN' if dry else 'EXECUTE'} ===")
    log(f"Root: {root}")
    log("بحث عن backup files...")
    bfs = find_backups(root)
    log(f"وُجد {len(bfs)} ملف")
    for f in bfs:
        move(f, vault / "files" / f.relative_to(root), dry)
    log("بحث عن archive folders...")
    afs = find_archives(root)
    log(f"وُجد {len(afs)} مجلد")
    for f in afs:
        move(f, archive / f.relative_to(root), dry)
    log("بحث عن full backup folders...")
    fbs = find_full_backups(root)
    log(f"وُجد {len(fbs)} مجلد")
    for f in fbs:
        move(f, archive / f.relative_to(root), dry)
    if not dry:
        rp = root / VAULT_FOLDER / f"cleanup_report_{ts}.txt"
        rp.parent.mkdir(parents=True, exist_ok=True)
        with open(rp, "w", encoding="utf-8") as fh:
            fh.write(f"Cleanup Report\nTS: {ts}\nBackups: {len(bfs)}\nArchives: {len(afs)}\nFullBackups: {len(fbs)}\n")
        log(f"📝 تقرير محفوظ: {rp}")
    log("✅ تم")
if __name__ == "__main__":
    main()