CREATE TABLE ai.recipes
(
    key         TEXT        NOT NULL,
    raw_data    JSONB       NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recipes_key
    ON ai.recipes (key);