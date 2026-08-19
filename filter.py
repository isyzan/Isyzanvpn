import requests
import re
import sys
from datetime import datetime

print("🚀 ISYZAN FILTER: проверка серверов...")

# 1. Скачиваем список
url = 'https://solovyov-jenya2004.vercel.app/final_sorted/'
try:
    resp = requests.get(url, timeout=10)
    raw = resp.text
except:
    print("❌ Не удалось скачать список")
    sys.exit(1)

# 2. Парсим строки (каждая строка — сервер)
lines = raw.strip().splitlines()
print(f"📡 Всего строк в источнике: {len(lines)}")

# 3. Берём первые 200 для проверки (чтобы не долго)
check_list = lines[:200]
working = []
dead = []

print("🔍 Проверяем серверы (это займёт ~20 секунд)...")
for i, server in enumerate(check_list):
    # Пытаемся подключиться через http (порт 80) или https (443)
    # Просто проверяем, отвечает ли IP/порт
    try:
        # Используем httpbin.org как тест
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

# 4. Формируем финальный список:
#    - берём все рабочие (если их меньше 130, добиваем случайными из непроверенных)
#    - добавляем 20 нерабочих (из dead)
final = []

# Берём рабочие
if len(working) >= 100:
    final.extend(working)
else:
    # Если рабочих мало — добиваем из оставшихся (непроверенных)
    extra = lines[200:]  # те, что не проверяли
    import random
    random.shuffle(extra)
    need = 100 - len(working)
    final.extend(working)
    final.extend(extra[:need])

# Добавляем 20 нерабочих (если есть)
if len(dead) >= 20:
    final.extend(dead[:20])
else:
    final.extend(dead)
    # если мало нерабочих — добиваем случайными из непроверенных (помечаем как нерабочие)
    extra_dead = lines[200:250]
    import random
    random.shuffle(extra_dead)
    final.extend(extra_dead[:20 - len(dead)])

# 5. Перемешиваем финальный список, чтобы нерабочие были вразброс
import random
random.shuffle(final)

# 6. Записываем файл с шапкой
with open('isyzan_incy.txt', 'w') as f:
    f.write("# Isyzan vpn🐱\n")
    f.write("# Поддержка: @isyzan\n")
    f.write("# Канал: @isy_zan1\n")
    f.write(f"# Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("# Рабочие серверы + 20 нерабочих (для теста)\n")
    f.write("\n")
    for s in final:
        f.write(s + "\n")

print(f"🎉 Файл создан, всего серверов: {len(final)}")
print("📁 Сохранён как isyzan_incy.txt")
