import argparse
import os
from datetime import datetime
from step1 import validate_path
from step2 import scan_folder
from step3 import add_hashes, find_duplicates
from step4 import compare_folders

def filter_by_extension(files, ext):
    """Возвращает список файлов, у которых расширение соответствует ext (без точки)."""
    if not ext:
        return files
    ext = ext.lower()
    if not ext.startswith('.'):
        ext = '.' + ext
    return [f for f in files if os.path.splitext(f['rel'])[1].lower() == ext]

def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', help='Source folder')
    p.add_argument('backup', nargs='?', help='Backup folder (optional)', default=None)
    p.add_argument('--ext', help='Filter by extension (e.g., txt)', default=None)
    args = p.parse_args()

    src_path = validate_path(args.source)
    files = scan_folder(src_path)
    files = filter_by_extension(files, args.ext)
    files = add_hashes(files)
    dups = find_duplicates(files)

    if args.ext:
        print(f"\nФильтр по расширению: .{args.ext.lstrip('.')}")

    print(f"\nНайдено файлов: {len(files)}")
    for f in sorted(files, key=lambda x: x['rel']):
        dt = datetime.fromtimestamp(f['mtime']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nФайл: {f['rel']}\n  Размер: {f['size']} байт\n  Изменён: {dt}")

    print(f"\nУникальных файлов: {len(set(f['hash'] for f in files))}")
    print(f"Групп дубликатов: {len(dups)}")

    for i, (h, paths) in enumerate(dups.items(), 1):
        print(f"\nДубликаты #{i} (хэш: {h[:16]}...):")
        for path in paths:
            print(f"  - {path}")

    if args.backup:
        bak_path = validate_path(args.backup)
        bak_files = scan_folder(bak_path)
        bak_files = filter_by_extension(bak_files, args.ext)
        bak_files = add_hashes(bak_files)
        missing, modified, extra = compare_folders(files, bak_files)
        s = {f['rel']: f['hash'] for f in files}
        b = {f['rel']: f['hash'] for f in bak_files}
        identical = sum(1 for r in s if r in b and s[r] == b[r])
        print(f"\nСравнение с резервной копией:\n  Исходная: {src_path}\n  Бэкап: {bak_path}")
        if args.ext:
            print(f"  (фильтр по расширению .{args.ext.lstrip('.')} применён к обеим папкам)")
        print(f"\nОтсутствуют в бэкапе:\n  " + ("\n  ".join(sorted(missing)) if missing else "нет"))
        print(f"\nИзменены:\n  " + ("\n  ".join(sorted(modified)) if modified else "нет"))
        print(f"\nЛишние в бэкапе:\n  " + ("\n  ".join(sorted(extra)) if extra else "нет"))
        print(f"\nИдентичных файлов: {identical}")

if __name__ == '__main__':
    main()
