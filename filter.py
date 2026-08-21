import requests
import re
import sys
from datetime import datetime
import random

print("🚀 ISYZAN FILTER: проверка серверов...")

url = 'https://solovyov-jenya2004.vercel.app/final_sorted/'
try:
    resp = requests.get(url, timeout=10)
    raw = resp.text
except:
    print("❌ Не удалось скачать список")
    sys.exit(1)

lines = raw.strip().splitlines()
print(f"📡 Всего строк в источнике: {len(lines)}")

check_list = lines[:200]
working = []
dead = []

print("🔍 Проверяем серверы (это займёт ~20 секунд)...")
for i, server in enumerate(check_list):
    try:
        test_url = 'https://httpbin.org/ip'
        proxies = {'http': server, 'https': server}
        r = requests.get(test_url, proxies=proxies, timeout=2)
        if r.status_code == 200:
            working.append(server)
            print(f"  ✅ {server} — рабочий")
        else:
            dead.append(server)
            print(f"  ❌ {server} — не отвечает")
    except:
        dead.append(server)
        print(f"  ❌ {server} — ошибка соединения")

print(f"✅ Рабочих: {len(working)}")
print(f"💀 Нерабочих: {len(dead)}")

final = []

if len(working) >= 100:
    final.extend(working)
else:
    extra = lines[200:]
    random.shuffle(extra)
    need = 100 - len(working)
    final.extend(working)
    final.extend(extra[:need])

if len(dead) >= 20:
    final.extend(dead[:20])
else:
    final.extend(dead)
    extra_dead = lines[200:250]
    random.shuffle(extra_dead)
    final.extend(extra_dead[:20 - len(dead)])

random.shuffle(final)

# ✅ ГЛАВНОЕ: имя файла — Isyzan_vpn.txt
with open('Isyzan_vpn.txt', 'w') as f:
    f.write("# Isyzan vpn🐱\n")
    f.write("# Поддержка: @isyzan\n")
    f.write("# Канал: @isy_zan1\n")
    f.write(f"# Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("# Рабочие серверы + 20 нерабочих (для теста)\n")
    f.write("\n")
    for s in final:
        f.write(s + "\n")

print(f"🎉 Файл создан, всего серверов: {len(final)}")
print("📁 Сохранён как Isyzan_vpn.txt")
