# 7DTD AI Core — Roadmap v3 (API + log files + AI orchestration)

## 🏗️ Архитектура системы

- [ ] File-based log ingestion
- [ ] Event parser (log → structured events)
- [ ] Event bus (RabbitMQ + Taskiq)
- [ ] AI engine (Ollama / Llama 3)
- [ ] Intent layer (AI → JSON commands)
- [ ] Execution API layer (7DTD Web API / Alloc API)
- [ ] Safety gateway (whitelist + rate limit)
- [ ] PostgreSQL storage (players, events, AI decisions)

---

# 📄 1. Log ingestion (file watcher)

## Цель

Читать игровые логи напрямую из файла без stdout/sockets/docker stream.

## Задачи

- [ ] Определить путь к логам 7DTD
- [ ] Реализовать file tail reader (`tail -f` behavior)
- [ ] Поддержать чтение новых строк в realtime
- [ ] Обработать ротацию логов
- [ ] Добавить reconnect/reopen логики
- [ ] Нормализовать строки логов
- [ ] Игнорировать дубли при перезапуске

## Технологии

- `aiofiles`
- `watchfiles` / `watchdog`
- async tasks

---

# 🧠 2. Event parser

## Цель

Преобразовывать сырые строки логов в структурированные события.

## Задачи

- [ ] Разделить лог на типы событий:
  - [ ] chat messages
  - [ ] player join
  - [ ] player leave
  - [ ] deaths
  - [ ] system warnings
  - [ ] errors
  - [ ] anticheat events

- [ ] Реализовать regex/parser layer
- [ ] Добавить SteamID extraction
- [ ] Добавить player name extraction
- [ ] Добавить timestamp normalization
- [ ] Преобразование:
  ```json
  raw log -> structured event
  ```

## Пример event

```json
{
  "event_type": "chat_message",
  "steam_id": "7656119...",
  "player_name": "Player",
  "message": "hello",
  "timestamp": "2026-05-16T10:00:00Z"
}
```

---

# 📨 3. Event Bus Layer (RabbitMQ + Taskiq)

## Цель

Асинхронное разделение ingestion, AI и execution.

## RabbitMQ

- [ ] Поднять RabbitMQ broker
- [ ] Создать exchange:
  - `7dtd.events`

## Queues

- [ ] `logs_queue`
- [ ] `ai_queue`
- [ ] `execution_queue`
- [ ] `analytics_queue`

## Workers

- [ ] `log_worker`
- [ ] `ai_worker`
- [ ] `command_worker`
- [ ] `analytics_worker`

## Задачи

- [ ] Event publishing
- [ ] Retry policies
- [ ] Dead-letter queues
- [ ] Backpressure handling

---

# 🤖 4. AI engine (Ollama)

## Цель

AI анализирует события и предлагает действия.

## Задачи

- [ ] Подключить Ollama async client
- [ ] Настроить model manager
- [ ] Подготовить system prompt:
  - server admin role
  - moderation role
  - assistant role

- [ ] Ограничить output:
  - только JSON
  - без свободного текста

- [ ] Реализовать:
  - intent classification
  - moderation analysis
  - behavior analysis
  - decision generation

## Возможные модели

- [ ] Llama 3
- [ ] Gemma
- [ ] Mistral

---

# 🧾 5. Intent layer

## Цель

AI не выполняет команды напрямую.

AI генерирует только intents.

## Пример intents

- [ ] `welcome_player`
- [ ] `say_message`
- [ ] `warn_player`
- [ ] `mute_player`
- [ ] `kick_player`
- [ ] `ban_player`

## Задачи

- [ ] JSON schema validation
- [ ] Confidence score
- [ ] Intent normalization
- [ ] Intent audit logging
- [ ] Reject invalid AI responses

## Пример

```json
{
  "intent": "warn_player",
  "target": "7656119...",
  "reason": "spam",
  "confidence": 0.92
}
```

---

# ⚙️ 6. Execution API layer (7DTD)

## Цель

Безопасное выполнение команд через API.

## Задачи

- [ ] Подключить 7DTD Web API
- [ ] Поддержать Alloc API
- [ ] Настроить auth:
  - `X-SDTD-API-TOKENNAME`
  - `X-SDTD-API-SECRET`

- [ ] Реализовать executor:
  - say
  - kick
  - ban
  - whitelist
  - teleport (if supported)

- [ ] Timeout handling
- [ ] Retry handling
- [ ] Error normalization

---

# 🔐 7. Safety gateway

## Цель

AI не должен иметь прямого контроля над сервером.

## Задачи

- [ ] Whitelist разрешённых команд
- [ ] Confidence threshold
- [ ] Rate limiting
- [ ] Cooldowns на punish actions
- [ ] AI action logging
- [ ] Manual approve mode
- [ ] Disable AI execution mode
- [ ] Emergency stop

## Дополнительно

- [ ] Защита от prompt injection
- [ ] Ограничение dangerous intents
- [ ] Проверка аргументов команд

---

# 🧾 8. Database (PostgreSQL)

## Таблицы

### players

- [ ] SteamID
- [ ] nickname history
- [ ] first_seen
- [ ] last_seen
- [ ] total_sessions

### events

- [ ] raw logs
- [ ] parsed events
- [ ] chat messages
- [ ] server events

### ai_decisions

- [ ] intent
- [ ] confidence
- [ ] AI response
- [ ] execution result

### sessions

- [ ] player joins/leaves
- [ ] online duration

---

# 🧠 9. AI automation features

## Moderation

- [ ] Spam detection
- [ ] Toxicity detection
- [ ] Flood detection
- [ ] Suspicious behavior detection

## Automation

- [ ] Auto welcome messages
- [ ] Auto warnings
- [ ] Daily server summary
- [ ] AI admin assistant
- [ ] Event summarization

## Analytics

- [ ] Peak online tracking
- [ ] Active players statistics
- [ ] Chat activity analysis

---

# 📊 10. Control & Monitoring

## Admin tools

- [ ] Telegram bot (aiogram)
- [ ] Live log viewer
- [ ] AI decision feed
- [ ] Manual command execution
- [ ] AI override panel

## Monitoring

- [ ] RabbitMQ monitoring
- [ ] Worker healthchecks
- [ ] API latency metrics
- [ ] AI response timing
- [ ] Server health monitoring

---

# 🧱 11. Suggested project structure

```text
src/
├── application/
├── domain/
├── infrastructure/
│   ├── ai/
│   ├── api/
│   ├── db/
│   ├── logs/
│   ├── messaging/
│   └── monitoring/
├── presentation/
├── workers/
└── shared/
```

---

# ⚓ Ключевая архитектурная идея

- [ ] AI НЕ выполняет команды напрямую
- [ ] AI только генерирует intent
- [ ] Execution layer полностью отделён
- [ ] Все действия проходят через safety gateway
- [ ] Log ingestion отделён от AI
- [ ] RabbitMQ используется как центральная event шина