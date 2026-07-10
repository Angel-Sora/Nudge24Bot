# Nudge24Bot 🤖

Telegram-бот для дизайнеров, который помогает сохранять продуктивность и избегать выгорания с помощью AI и Google Sheets.

---

## 📖 О проекте

**Nudge24Bot** — это умный помощник, который каждое утро даёт персонализированное задание на основе твоего настроения, профессии и целей. Вечером бот проверяет, сделал ли ты задание, и отслеживает динамику настроения.

Бот работает в **Telegram** и использует **Google Sheets** для хранения данных и **Google Gemini AI** для генерации заданий.

### Ключевые возможности:
- 🌤 **Утренний опрос** — оцени настроение, получи задание от AI
- 🎯 **Персонализация** — задания адаптируются под твою профессию и цели
- 🌙 **Вечерний чек** — проверка выполнения и отслеживание прогресса
- 📊 **Аналитика** — все данные сохраняются в Google Sheets
- 🧠 **AI генерация** — задания создаются с помощью Google Gemini

---

## 🚀 Установка и запуск

### Требования:
- Python 3.8+
- Telegram Bot Token (от @BotFather)
- Google Gemini API Key
- Google Sheets API (credentials.json)
- Аккаунт на [Replit.com](https://replit.com) (для бесплатного хостинга) или любой VPS

### Шаг 1: Клонирование
```bash
git clone https://github.com/Angel-Sora/Nudge24Bot.git
cd Nudge24Bot
```
### Шаг 2: Установка зависимостей
```bash
pip install -r requirements.txt
```
### Шаг 3: Настройка переменных окружения
Создай файл .env:

.env
```bash
BOT_TOKEN=твой_токен_бота
GEMINI_API_KEY=твой_ключ_gemini
SPREADSHEET_ID=id_твоей_таблицы
```
### Шаг 4: Настройка Google Sheets API
4.1 Создай сервисный аккаунт:
Перейди в Google Cloud Console

Создай новый проект или выбери существующий

Включи Google Sheets API и Google Drive API

Перейди в "Credentials" → "Create Credentials" → "Service Account"

Заполни имя и нажми "Create"

Нажми на созданный сервисный аккаунт → "Keys" → "Add Key" → "Create New Key"

Выбери JSON и скачай файл

4.2 Получи CREDENTIALS_JSON:
Открой скачанный JSON-файл в блокноте и скопируй ВСЁ содержимое (весь JSON-объект).

4.3 Настройка CREDENTIALS_JSON:
Если используешь Replit:

Перейди в "Secrets" (вкладка с замком)

Нажми "Add new secret"

Key: CREDENTIALS_JSON

Value: вставь весь скопированный JSON из файла credentials.json

Сохрани

Если запускаешь локально:

Сохрани скачанный файл как credentials.json в папке проекта

Убедись, что файл есть в той же папке, что и bot.py

4.4 Предоставь доступ к таблице:
Открой свою Google Sheets таблицу

Нажми "Share" (Поделиться)

Скопируй email из поля "Client Email" в твоём credentials.json

Вставь этот email в поле "Add people" и дай права Редактор

Нажми "Send"

### Шаг 5: Получение SPREADSHEET_ID
Открой свою Google Sheets таблицу

Посмотри на URL: https://docs.google.com/spreadsheets/d/***ЭТОТ_ID***/edit

Скопируй ID между /d/ и /edit

Вставь его в .env файл

### Шаг 6: Запуск
```bash
python bot.py
```
## 🌐 Деплой на Replit (рекомендуемый способ)
Replit — это бесплатный хостинг для Python-ботов, который работает 24/7.

6.1 Создание Replit:
Зарегистрируйся на Replit.com

Нажми "Create Repl" → "Import from GitHub"

Вставь ссылку: https://github.com/Angel-Sora/Nudge24Bot.git

Нажми "Import"

6.2 Настройка Secrets в Replit:
В левом меню нажми на иконку замка (Secrets)

Добавь следующие переменные:

BOT_TOKEN = твой токен

GEMINI_API_KEY = твой ключ Gemini

SPREADSHEET_ID = ID таблицы

CREDENTIALS_JSON = весь JSON из credentials.json

6.3 Запуск в Replit:
Нажми "Run" (зелёная кнопка)

Бот запустится и будет работать

Чтобы бот работал 24/7, включи "Always On" (нужна подписка Hacker) или используй UptimeRobot для пингования твоего Replit каждые 5 минут

6.4 Если бот не запускается в Replit:
Проверь, что все Secrets добавлены правильно

Убедись, что в CREDENTIALS_JSON нет лишних пробелов и переносов строк

Нажми "Stop" и снова "Run"

Проверь логи в консоли (вкладка "Console")

## 🤖 Как бот работает в Telegram
Создание бота в Telegram:
Найди в Telegram @BotFather

Отправь команду /newbot

Придумай имя боту (например, "Nudge24 Bot")

Придумай username (должен заканчиваться на bot, например Nudge24Bot)

BotFather пришлёт токен — сохрани его!

Вставь этот токен в BOT_TOKEN

Где найти бота:
Твой бот будет доступен по ссылке: https://t.me/username_бота

Например: https://t.me/Nudge24Bot

Как пользоваться:
Напиши /start в чате с ботом

Бот предложит заполнить анкету

После заполнения анкеты, нажми «Оценить настроение»

Получи задание на день

Вечером бот сам спросит про выполнение

## 🏗 Архитектура

```
Nudge24Bot/
├── bot.py              # Основной файл с логикой бота
├── ai_helper.py        # Интеграция с Google Gemini AI
├── database.py         # Работа с Google Sheets
├── config.py           # Конфигурация и переменные окружения
├── requirements.txt    # Зависимости
├── .env                # Переменные окружения (не в репозитории)
├── credentials.json    # JSON сервисного аккаунта (не в репозитории)
└── README.md           # Документация
```
## 🎮 Как пользоваться ботом
### 1. Старт
Напиши /start — бот предложит заполнить анкету.

### 2. Анкета
Перейди по ссылке и укажи:

Профессию

Цель (чего хочешь достичь)

Доступное время

### 3. Утро
Нажми «Оценить настроение» и выбери цифру от 1 до 10. Бот пришлёт задание на день.

### 4. Вечер
Бот сам спросит:

Сделал ли ты задание?

Какое у тебя настроение вечером?

### 5. Аналитика
Все данные сохраняются в Google Sheets. Ты можешь видеть свою динамику и прогресс.

## 🛠 Технологии
Компонент	Технология
Telegram Bot	python-telegram-bot v20.7
AI	Google Gemini AI
База данных	Google Sheets (gspread)
Авторизация	OAuth2 / Service Account
Переменные окружения	python-dotenv
Хостинг	Replit / VPS
📊 Формат данных в Google Sheets
Колонка	Описание
user_id	ID пользователя в Telegram
username	Имя пользователя
profession	Профессия
goal	Цель
time_available	Доступное время
morning_mood	Настроение утром (1-10)
morning_time	Время утреннего опроса
evening_mood	Настроение вечером (1-10)
evening_time	Время вечернего чека
task_completed	Выполнено задание? (Да/Нет)
current_task	Текущее задание
registered_at	Дата регистрации
🤖 AI Prompts
Бот использует разные промпты в зависимости от настроения:

Настроение 8-10: задание на закрепление успеха

Настроение 5-7: лёгкое задание для поднятия энергии

Настроение 1-4: супер-лёгкое задание для расслабления

## 🔒 Переменные окружения
Переменная	Описание	Где взять
BOT_TOKEN	Токен Telegram бота	От @BotFather
GEMINI_API_KEY	Ключ Google Gemini AI	Google AI Studio
SPREADSHEET_ID	ID Google Sheets таблицы	Из URL таблицы
CREDENTIALS_JSON	JSON сервисного аккаунта	Из Google Cloud Console
## ⚠️ Важные моменты
CREDENTIALS_JSON — это весь JSON-объект из скачанного файла credentials.json (включая все скобки и кавычки)

Не добавляй этот файл в репозиторий (добавь в .gitignore)

Для локального запуска используй файл credentials.json

Для Replit используй переменную CREDENTIALS_JSON в Secrets

Убедись, что сервисному аккаунту даны права на редактирование таблицы

Бот работает только в Telegram — для взаимодействия нужен аккаунт в Telegram

## 🐛 Частые проблемы и их решение
1. Бот не отвечает в Telegram
Проверь, что бот запущен (консоль показывает "🤖 Бот запущен!")

Проверь токен в .env

Проверь интернет-соединение

2. Ошибка "CREDENTIALS_JSON не найдена"
На Replit: добавь переменную в Secrets

Локально: создай файл credentials.json в папке проекта

3. Ошибка "Table not found"
Проверь SPREADSHEET_ID

Убедись, что таблица существует и у сервисного аккаунта есть доступ

4. Бот не запускается на Replit
Проверь все Secrets

Убедись, что в .replit файле указан правильный entrypoint: python bot.py

Нажми "Stop" → "Run" заново

## 🙏 Благодарности

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — отличная библиотека для Telegram
- [Google Gemini AI](https://ai.google.dev/) — генерация заданий
- [gspread](https://docs.gspread.org/) — работа с Google Sheets
- [Replit](https://replit.com) — бесплатный хостинг

## 👨‍💻 Автор
Angel-Sora


# ⭐ Поставь звезду, если проект полезен!
