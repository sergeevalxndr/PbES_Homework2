import Engine

try:
    engine = Engine.PokemonEngine()
    #engine.run_tournament(64)  # Запуск чемпионата, где покемоны бьются насмерть до последнего выжившего
    engine.run_training(6, 20)  # Запуск тренировки, где покемоны бьются между собой
except Exception as ex:
    print(ex)


# TODO Добавить персонажей/эффекты
# TODO Заряд способностей
# TODO Добавить вывод эффектов
# TODO Добавить файловый вывод
# TODO Разобрать приватность полей/методов

