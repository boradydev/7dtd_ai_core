-- :text
-- :file
-- :limit
-- :threshold

WITH search AS (SELECT r.key,
                       l.__SEARCH_COLUMN__                    AS name,

                       TS_RANK(
                               TO_TSVECTOR('__SEARCH_LANG__', l.__SEARCH_COLUMN__),
                               websearch_to_tsquery('__SEARCH_LANG__', :text)
                       )                                      AS fts_score,

                       similarity(l.__SEARCH_COLUMN__, :text) AS trigram_score

                FROM ai.recipes AS r
                         JOIN ai.localization AS l
                              ON r.key = l.key

                WHERE l.file = :file
                  AND (
                    TO_TSVECTOR('__SEARCH_LANG__', l.__SEARCH_COLUMN__)
                        @@ websearch_to_tsquery('__SEARCH_LANG__', :text)
                        OR
                    similarity(l.__SEARCH_COLUMN__, :text) >= :threshold
                    ))

SELECT *,
       fts_score * 0.7 +
       trigram_score * 0.3 AS total_score
FROM search
ORDER BY total_score DESC
LIMIT :limit;
