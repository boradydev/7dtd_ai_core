-- Params:
-- :player_id
-- :history

INSERT INTO ai.chat_histories (player_id, history, updated_at)
VALUES (
    :player_id,
    CAST(:history AS jsonb),
    NOW()
)
ON CONFLICT (player_id)
DO UPDATE SET
    history = EXCLUDED.history,
    updated_at = NOW();
