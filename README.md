# Akbarloh Browser Page

Простая статическая страница `index.html` в стиле «браузер в браузере».

Сейчас интерфейс оформлен в стиле **Scramjet** и стартует с **DuckDuckGo** внутри окна.

## Важно

Файл **уже добавлен в репозиторий проекта**: `index.html`.
Если ты имел в виду `idex.html`, скорее всего это опечатка — правильное имя файла: **`index.html`**.

---

## Как скачать `index.html`

### Способ 1: Скачать весь репозиторий (рекомендуется)
```bash
git clone https://github.com/YOUR_USERNAME/akbarloh-browser.git
cd akbarloh-browser
```
После этого файл будет здесь:
- `./index.html`

### Способ 2: Скачать только один файл с GitHub
1. Открой файл `index.html` в репозитории на GitHub.
2. Нажми **Raw**.
3. Сохрани страницу как `index.html` (Ctrl+S).

Прямая ссылка обычно такого вида:
- `https://raw.githubusercontent.com/YOUR_USERNAME/akbarloh-browser/main/index.html`

### Способ 3: Скачать ZIP
1. На странице репозитория нажми **Code** → **Download ZIP**.
2. Распакуй архив.
3. Возьми файл `index.html`.

---


## Почему некоторые сайты могут работать нестабильно внутри окна

Страница использует ваш `proxy_server.py`, поэтому сайт загружается внутри окна браузера через `/proxy?url=...` и работает лучше, чем прямой `iframe`.

Важно: отдельные сайты всё равно могут ограничивать доступ (бот-защита, авторизация, сложные JS-проверки).

Если хотите «полный серверный режим», запускайте именно `python3 proxy_server.py` (а не GitHub Pages).

---

## Как запустить локально

### Вариант 1: Python (самый простой)
```bash
python3 proxy_server.py
```
После запуска открой:
- http://localhost:4173

Остановка сервера: `Ctrl + C`.

### Вариант 2: Просто открыть файл
Можно открыть `index.html` напрямую двойным кликом, но лучше через сервер (как выше), чтобы поведение было ближе к реальному хостингу.

---

## Как закинуть это на GitHub repository

### 1) Создай пустой репозиторий на GitHub
Например: `akbarloh-browser`.

### 2) Привяжи локальный репозиторий к GitHub
Замените `YOUR_USERNAME` и имя репозитория:
```bash
git remote add origin https://github.com/YOUR_USERNAME/akbarloh-browser.git
```

Если remote уже существует:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/akbarloh-browser.git
```

### 3) Отправь код
Для ветки `main`:
```bash
git push -u origin main
```

Если у тебя ветка называется `work` (или другая), можно так:
```bash
git push -u origin work
```

> Если GitHub спросит логин/пароль, используй Personal Access Token (PAT) вместо пароля.

---

## Как зайти на GitHub Pages

### Включение GitHub Pages
1. Открой репозиторий на GitHub.
2. `Settings` → `Pages`.
3. В `Source` выбери **Deploy from a branch**.
4. Выбери ветку:
   - `main` (или нужную ветку),
   - папку `/ (root)`.
5. Нажми **Save**.
6. Подожди 1–3 минуты.

Сайт будет доступен по адресу:
- `https://YOUR_USERNAME.github.io/akbarloh-browser/`

Если не открывается сразу — обнови через 1–2 минуты.

---

## Частые проблемы

- **404 на GitHub Pages**: проверь, что `index.html` лежит в корне репозитория.
- **Страница не обновилась**: подожди пару минут и сделай hard refresh (`Ctrl+F5`).
- **Нет прав на push**: убедись, что ты владелец репозитория или добавлен как collaborator.

---

## Полезные команды

Проверить текущую ветку:
```bash
git branch --show-current
```

Проверить remote:
```bash
git remote -v
```
