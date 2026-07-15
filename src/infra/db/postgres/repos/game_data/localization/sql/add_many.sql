-- Params:
-- :key
-- :file
-- :type
-- :used_in_main_menu
-- :no_translate
-- :keep_loaded
-- :english
-- :context
-- :german
-- :spanish
-- :french
-- :italian
-- :japanese
-- :koreana
-- :polish
-- :brazilian
-- :russian
-- :turkish
-- :schinese
-- :tchinese

INSERT INTO ai.localization (
    key,
    file,
    type,
    used_in_main_menu,
    no_translate,
    keep_loaded,
    english,
    context,
    german,
    spanish,
    french,
    italian,
    japanese,
    koreana,
    polish,
    brazilian,
    russian,
    turkish,
    schinese,
    tchinese
)
VALUES (
    :key,
    :file,
    :type,
    :used_in_main_menu,
    :no_translate,
    :keep_loaded,
    :english,
    :context,
    :german,
    :spanish,
    :french,
    :italian,
    :japanese,
    :koreana,
    :polish,
    :brazilian,
    :russian,
    :turkish,
    :schinese,
    :tchinese
);
