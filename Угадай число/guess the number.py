import numpy as np
number = np.random.randint(1,101) 
print ("Загадано число от 1 до 100")


def game_core_v5(number):
    count = 0
    predict = 50 
    array = [25,10,5,4,3,2,1]
    while number != predict:
        for i in array:
            count += 1
            if number >= predict+i: 
                predict += i
                if number == predict:
                    break
            elif number <= predict-i: 
                predict -= i
                if number == predict:
                    break
    return(count)

def score_game(game_core):
    '''Запускаем игру 1000 раз, чтоб узнать как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score}({np.mean(count_ls)}) попыток")

score_game(game_core_v5)