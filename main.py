import Engine

try:
    engine = Engine.PokemonEngine(64)
    engine.run()
except Exception as ex:
    print(ex)


# TODO Добавить эффекты/способности
# TODO Заряд способностей
# TODO Добавить файловый вывод
# TODO Разобрать приватность полей/методов

