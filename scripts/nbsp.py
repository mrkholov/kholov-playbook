# -*- coding: utf-8 -*-
"""Расстановка неразрывных пробелов в русском тексте HTML-страницы.
Работает только с текстовыми узлами: содержимое тегов, script и style не трогает."""
import io, re, sys

NB = ' '

SHORT = ("в во а и к ко о об обо с со у из изо за на над до от ото по под подо при про без для "
         "не ни же ли бы то что как но да или ещё уже их им ей ею её его им мы вы я он она они "
         "через между около перед после чтобы если чем тем так вот там тут").split()
SHORT_RE = re.compile(r'(?<![^\s(«"„\-–—/])(' + '|'.join(sorted(SHORT, key=len, reverse=True)) + r') +(?=[^\s])',
                      re.IGNORECASE)

UNITS = ("млн млрд тыс человек человека людей раз раза лет года год дней дня месяц месяца месяцев "
         "часов часа час п мес чел").split()
NUM_UNIT_RE = re.compile(r'(\d) +(?=(?:' + '|'.join(UNITS) + r')\b)')

def fix(t):
    t = SHORT_RE.sub(lambda m: m.group(1) + NB, t)
    t = NUM_UNIT_RE.sub(lambda m: m.group(1) + NB, t)
    t = re.sub(r' +(?=[—–] )', NB, t)          # неразрывный пробел перед тире
    t = re.sub(r'(\d) +(%)', lambda m: m.group(1) + NB + m.group(2), t)
    return t

path = sys.argv[1]
src = io.open(path, encoding='utf-8').read()
parts = re.split(r'(<[^>]*>)', src)
skip = False
out = []
for p in parts:
    if p.startswith('<'):
        low = p.lower()
        if low.startswith('<script') or low.startswith('<style'):
            skip = True
        elif low.startswith('</script') or low.startswith('</style'):
            skip = False
        out.append(p)
    else:
        out.append(p if skip else fix(p))
res = ''.join(out)
io.open(path, 'w', encoding='utf-8').write(res)
print('неразрывных пробелов:', res.count(NB))
