CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE TABLE ai.localization
(
    key               TEXT        NOT NULL,

    file              TEXT,
    type              TEXT,

    used_in_main_menu BOOLEAN,
    no_translate      BOOLEAN,
    keep_loaded       BOOLEAN,

    english           TEXT        NOT NULL,
    context           TEXT,

    german            TEXT,
    spanish           TEXT,
    french            TEXT,
    italian           TEXT,
    japanese          TEXT,
    koreana           TEXT,
    polish            TEXT,
    brazilian         TEXT,
    russian           TEXT,
    turkish           TEXT,
    schinese          TEXT,
    tchinese          TEXT,

    imported_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_localization_key
    ON ai.localization (key);

CREATE INDEX idx_localization_english_trgm
    ON ai.localization USING gin (english gin_trgm_ops);

CREATE INDEX idx_localization_russian_trgm
    ON ai.localization USING gin (russian gin_trgm_ops);
