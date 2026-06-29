import os

def scan_folder(root):
    files = []

    def walk_dir(dirpath, rel_prefix=''):
        """Рекурсивно обходит папку, используя os.listdir."""
        try:
            entries = os.listdir(dirpath)
        except PermissionError:
            # Если нет доступа к папке, пропускаем её
            return

        for name in entries:
            full_path = os.path.join(dirpath, name)
            # Пропускаем символические ссылки
            if os.path.islink(full_path):
                continue

            if os.path.isfile(full_path):
                stat = os.stat(full_path)
                rel = os.path.join(rel_prefix, name) if rel_prefix else name
                files.append({
                    'path': full_path,
                    'rel': rel,
                    'size': stat.st_size,
                    'mtime': stat.st_mtime
                })
            elif os.path.isdir(full_path):
                new_rel = os.path.join(rel_prefix, name) if rel_prefix else name
                walk_dir(full_path, new_rel)

    walk_dir(root)
    return files