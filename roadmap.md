# 7DTD AI Core — Roadmap v2 (API + stdout + AI orchestration)

## 🏗️ Архитектура системы

- [ ] Docker stdout ingestion (без файлов)
- [ ] Event parser (log → structured events)
- [ ] Event bus (asyncio.Queue / Redis)
- [ ] AI engine (Ollama / Llama 3)
- [ ] Intent layer (AI → JSON commands)
- [ ] Execution API layer (7DTD Web API / Alloc API)
- [ ] Safety gateway (whitelist + rate limit)
- [ ] PostgreSQL storage (players, events, AI decisions)

---

## 📡 1. Log ingestion (stdout stream)

- [ ] Подключить чтение логов через `docker logs -f`
- [ ] Реализовать streaming reader (async/subprocess)
- [ ] Обрабатывать stdout в реальном времени
- [ ] Нормализовать входящие строки логов

---

## 🧠 2. Event parser

- [ ] Разделить лог на типы событий:
  - chat messages
  - player join/leave
  - system warnings
  - errors
- [ ] Преобразовать лог → structured event (JSON)
- [ ] Добавить SteamID extraction
- [ ] Добавить timestamp normalization

---

## Event Bus Layer (RabbitMQ + Taskiq)

- [ ] Поднять RabbitMQ broker
- [ ] Создать exchange: "7dtd.events"
- [ ] Разделить queues:
  - logs_queue
  - ai_queue
  - execution_queue
  - analytics_queue

- [ ] Подключить Taskiq workers:
  - log_worker
  - ai_worker
  - command_worker

---

## 🤖 4. AI engine (Ollama)

- [ ] Подключить Ollama async client
- [ ] Настроить system prompt (server admin role)
- [ ] Ограничить модель: только JSON output
- [ ] Реализовать intent classification
- [ ] Реализовать decision generation

---

## 🧾 5. Intent layer (ключевой слой)

- [ ] AI → structured JSON intent
- [ ] Пример intents:
  - welcome_player
  - ban_player
  - say_message
  - warn_player
- [ ] Добавить confidence score
- [ ] Запрет свободного текста в execution

---

## ⚙️ 6. Execution API layer (7DTD)

- [ ] Подключить 7DTD Web API (Alloc / vanilla)
- [ ] Настроить auth headers:
  - X-SDTD-API-TOKENNAME
  - X-SDTD-API-SECRET
- [ ] Реализовать командный executor:
  - say
  - kick
  - ban
  - teleport (if available)
- [ ] Обработка ошибок API

---

## 🔐 7. Safety gateway (обязательно)

- [ ] Whitelist разрешённых команд
- [ ] Rate limiting на команды
- [ ] Проверка confidence AI (> threshold)
- [ ] Логирование всех действий AI
- [ ] Manual override mode (disable AI exec)

---

## 🧾 8. Database (PostgreSQL)

- [ ] Таблица players (SteamID, name, last_seen)
- [ ] Таблица events (logs, chat, system)
- [ ] Таблица ai_decisions (intent, confidence, result)
- [ ] Таблица sessions (player sessions)

---

## 🧠 9. AI automation features

- [ ] Auto welcome messages
- [ ] Chat moderation (spam detection)
- [ ] Player behavior tracking
- [ ] Server event summarization
- [ ] AI daily report generator

---

## 📊 10. Control & monitoring (optional)

- [ ] Telegram bot admin panel (aiogram)
- [ ] Live log viewer
- [ ] Manual command execution
- [ ] AI decision override
- [ ] Server health monitoring

---

## ⚓ Ключевая архитектурная идея

- [ ] AI НЕ выполняет команды напрямую
- [ ] AI только генерирует intent (JSON)
- [ ] Execution layer полностью отделён
- [ ] Все действия проходят через safety gateway