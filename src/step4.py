def compare_folders(src, bak):
    # Словари для быстрого доступа по относительному пути
    s = {f['rel']: f for f in src}
    b = {f['rel']: f for f in bak}

    missing = []   # файлы, которые есть в источнике, но отсутствуют в бэкапе
    modified = []  # файлы, которые есть в обоих, но с разными хэшами
    extra = []     # файлы, которые есть только в бэкапе

    # Проходим по файлам источника
    for rel in s:
        if rel not in b:
            missing.append(rel)
        else:
            # Если хэши различаются – файл изменён
            if s[rel].get('hash') != b[rel].get('hash'):
                modified.append(rel)

    # Проходим по файлам бэкапа, чтобы найти лишние
    for rel in b:
        if rel not in s:
            extra.append(rel)

    return missing, modified, extra