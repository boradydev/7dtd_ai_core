CREATE SCHEMA ai;

CREATE TABLE ai.players
(
    player_id  TEXT PRIMARY KEY,
    nickname   TEXT        NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ai.chat_histories
(
    player_id    TEXT PRIMARY KEY,
    chat_history JSONB NOT NULL,

    CONSTRAINT fk_chat_histories_players
        FOREIGN KEY (player_id)
            REFERENCES ai.players (player_id)
);