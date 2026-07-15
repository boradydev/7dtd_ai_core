-- Params:
-- :key

SELECT key,
       raw_data
FROM ai.recipes
WHERE key = :key;
