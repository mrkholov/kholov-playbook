# -*- coding: utf-8 -*-
"""Собирает index.html в один самодостаточный файл для публикации по ссылке.

Картинки вшиваются в разметку как data-URI, внешние теги обёртки снимаются:
хостинг артефактов сам оборачивает содержимое в <!doctype html><head></head><body>.
"""
import base64, io, os, re, sys

SRC = 'index.html'
DST = sys.argv[1] if len(sys.argv) > 1 else 'artifact.html'

s = io.open(SRC, encoding='utf-8').read()

# 1. картинки внутрь файла
cache = {}
def inline(m):
    path = m.group(1)
    if path not in cache:
        data = open(path, 'rb').read()
        cache[path] = 'data:image/webp;base64,' + base64.b64encode(data).decode('ascii')
    return 'src="%s"' % cache[path]

s, n_img = re.subn(r'src="(assets/img/[^"]+)"', inline, s)

# 2. снимаем внешнюю обёртку — её добавляет хостинг
for tag in ('<!DOCTYPE html>', '<html lang="ru">', '<head>', '</head>',
            '<body>', '</body>', '</html>'):
    s = s.replace(tag + '\n', '').replace(tag, '')
# иконки лежат отдельными файлами — в самодостаточной версии их нет,
# у артефакта иконка задаётся при публикации
s = re.sub(r'<link rel="(?:apple-touch-)?icon"[^>]*>\n?', '', s)

s = re.sub(r'<meta charset="utf-8">\n?', '', s)
s = re.sub(r'<meta name="viewport"[^>]*>\n?', '', s)
s = s.strip() + '\n'

io.open(DST, 'w', encoding='utf-8').write(s)
size = os.path.getsize(DST)
print('картинок вшито: %d' % n_img)
print('%s — %.2f МБ' % (DST, size / 1e6))
assert '<html' not in s and '<body' not in s, 'обёртка снята не полностью'
assert size < 16e6, 'файл больше 16 МБ'
