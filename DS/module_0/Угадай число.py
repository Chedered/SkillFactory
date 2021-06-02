import numpy as np


def game_core_v5(number):
    """Ищем загадонное число через бинарный поиск.

    Определяем середину нашего диапазона чисел и сравниваем ее с нужныи числом.
    В зависимости от того, больше она или меньше нужного числа,
    дальнейший поиск осуществляется в нижней или в верхней половине нашего диапазона.
    Функция принимает загаданное число и возвращает число попыток.
    """
    count = 0
    low = 1
    high = 100
    mid = 0
    while number != mid:
        count += 1
        mid = (low + high) // 2
        if number < mid:
            high = mid - 1  # прибавляем\убаляем 1, так как серидина уже сравнивалась
        elif number > mid:
            low = mid + 1
    return count  # выход из цикла, если угадали


def score_game(game_core):
    """Запускаем игру 1000 раз, чтоб узнать как быстро игра угадывает число."""
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score}({np.mean(count_ls)}) попыток")


score_game(game_core_v5)
