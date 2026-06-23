CREATE SCHEMA ai;

CREATE TABLE ai.players
(
    player_id  TEXT PRIMARY KEY,
    nickname   TEXT        NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ai.chat_histories
(
    player_id  TEXT PRIMARY KEY,
    history    JSONB       NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);