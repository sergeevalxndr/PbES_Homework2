import Engine

try:
    engine = Engine.PokemonEngine(64)
    engine.run_tournament()
except Exception as ex:
    print(ex)


# TODO Добавить персонажей/эффекты
# TODO Исправить снятие эффектов
# TODO Заряд способностей
# TODO Добавить вывод эффектов
# TODO Добавить файловый вывод
# TODO Разобрать приватность полей/методов

