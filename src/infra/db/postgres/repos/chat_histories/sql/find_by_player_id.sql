-- Params:
-- :player_id

SELECT history
FROM ai.chat_histories
WHERE player_id = :player_id;
