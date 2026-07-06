CREATE TABLE ai.recipes
(
    name        TEXT        NOT NULL,
    raw_data    JSONB       NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recipes_name
    ON ai.recipes (name);