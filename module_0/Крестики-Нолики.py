# Игра "Крестики-Нолики"

# Объявляем переменные
field = [[" "] * 3 for i in range(3)]
crosses = ['X'] * 3
nulls = ['O'] * 3


def instruction():
    # Приветствие и инструкция
    print(' ')
    print('       Крестики-Нолики          ')
    print('           X  vs  O             ')
    print('--------------------------------')
    print(' Введите две цифры через пробел ')
    print('          от 1 до 3             ')
    print(' Первая цифра - номер строки    ')
    print(' Вторая цифра - номер столбца   ')
    print('--------------------------------')
    print('       Да начнется игра!        ')
    print(' ')


def output():
    # Рисуем игровое поле
    print('  | 1 | 2 | 3 |')
    for i, row in enumerate(field):
        print('-' * 15)
        row_str = str(i + 1) + ' | ' + ' | '.join(map(str, row)) + ' |'
        print(row_str)
    print('-' * 15)


def request():
    # Делаем ход
    # Проверяем корректность введенных данных
    while True:
        moves = input().split()

        # Проверка на количество введенных данных
        if len(moves) != 2:
            print('Неккоректный ввод!')
            print('Введите ДВЕ цифры')
            continue

        a, b = moves

        # Проверка на то, что веденные данные являются цифрами
        if not (a.isdigit()) or not (b.isdigit()):
            print('Неккоректный ввод!')
            print('Введите ЦИФРЫ')
            continue

        a, b = int(a), int(b)

        # Проверка на корректность введенных цифр
        if 1 > a or a > 3 or 1 > b or b > 3:
            print('Неккоректный ввод!')
            print('Введите ВЕРНЫЕ цифры')
            continue

        # Проверка на доступность клетки
        if field[a - 1][b - 1] != " ":
            print('Так уже ходили!')
            continue

        return a, b


def check_row():
    # Проверям выйгрыш по строке
    for i, row in enumerate(field):
        if row == crosses:
            field[i] = ['-'] * 3
            output()
            print(' ')
            print('Крестики победили!')
            return True
        if row == nulls:
            field[i] = ['-'] * 3
            output()
            print(' ')
            print('Нолики победили!')
            return True
    return False


def check_column():
    # Проверяем выйгрыш по столбцу
    for i in range(3):
        values = []
        for j in range(3):
            values.append(field[j][i])
        if values == crosses:
            for row in field:
                row[i] = '|'
            output()
            print(' ')
            print('Крестики победили!')
            return True
        if values == nulls:
            for row in field:
                row[i] = '|'
            output()
            print(' ')
            print('Нолики победили!')
            return True
    return False


def check_diag():
    # Проверяем выйгрыш по диагонали
    values = []
    for i in range(3):
        values.append(field[i][i])
    if values == crosses:
        for i, row in enumerate(field):
            row[i] = '\\'
        output()
        print(' ')
        print('Крестики победили!')
        return True
    if values == nulls:
        for i, row in enumerate(field):
            row[i] = '\\'
        output()
        print(' ')
        print('Нолики победили!')
        return True

    values = []
    for i in range(3):
        values.append(field[i][abs(i - 2)])
    if values == crosses:
        for i, row in enumerate(field):
            row[abs(i - 2)] = "/"
        output()
        print(' ')
        print('Крестики победили!')
        return True
    if values == nulls:
        for i, row in enumerate(field):
            row[abs(i - 2)] = "/"
        output()
        print(' ')
        print('Нолики победили!')
        return True

    return False


rounds = 0

instruction()

while True:
    output()

    rounds += 1

    if rounds % 2 == 1:
        print(' ')
        print('"Крестики", Ваш ход:')
        x, y = request()
        field[x - 1][y - 1] = 'X'
        print(' ')
    else:
        print(' ')
        print('"Нолики", Ваш ход:')
        x, y = request()
        field[x - 1][y - 1] = 'O'
        print(' ')

    if check_row():
        break

    if check_column():
        break

    if check_diag():
        break

    if rounds == 9:
        output()
        print(' ')
        print('Ничья!')
        break
