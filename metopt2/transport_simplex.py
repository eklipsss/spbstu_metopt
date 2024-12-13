import numpy as np

from north_west import north_west_corner
from prints import print_bfs, print_cycle, print_full_cycle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_us_and_vs(bfs, costs, step = 0):
    print("----------------------------------------")
    print(f"----ПОТЕНЦИАЛЫ на {step} шаге----")
    print("----------------------------------------")
    # выделим память под потенциалы
    us = [None] * len(costs)
    vs = [None] * len(costs[0])

    # первый потенциал u равен 0
    us[0] = 0

    # копируем допустимое базисное решение
    bfs_copy = bfs.copy()

    # пройдемся по базисному решению
    while len(bfs_copy) > 0:
        # index соответствует номеру элемента в базисном решении
        # bv соответствует индексам и значению в таблице
        for index, bv in enumerate(bfs_copy):
            # запомним индексы
            i, j = bv[0]
            # если потенцалам по данным индексам пустые, то ничего не делаем
            if us[i] is None and vs[j] is None: continue

            # запомним значение в таблице стоимостей
            cost = costs[i][j]
            # если не вычислили uᵢ
            if us[i] is None:
                # uᵢ = cᵢⱼ - vⱼ
                us[i] = cost - vs[j]
                print("u[" + str(i) + "] = " + str(-us[i]))

            # в обратном случае можем найти vⱼ
            else:
                # vⱼ = uᵢ - cᵢⱼ
                vs[j] = cost - us[i]
                print("v[" + str(j) + "] = " + str(vs[j]))
            bfs_copy.pop(index)
            break
    # возвращаем потенциалы поставищка и потребителя
    print("----------------------------------------")
    return us, vs


def get_ws(bfs, costs, us, vs):
    # вычислим параметр для свободных переменных
    ws = []
    # пройдемся по всем ячейкам стоимости
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            # вычислим параметр wᵢⱼ для каждой неосновной переменной
            # wᵢⱼ, где индексы не входят в базовое допустимое решение
            non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
            if non_basic:
                # wᵢⱼ = uᵢ + vⱼ - ciⱼ
                ws.append(((i, j), us[i] + vs[j] - cost))
    # возвращаем список хранящий индексы и значения параметра wᵢⱼ
    return ws


def can_be_improved(ws):
    for p, v in ws:
        # если хоть какое то wᵢⱼ больше нуля, значит решение не оптимально и его можно улучшить
        if v > 0:
            return True
    return False


def get_entering_variable_position(ws):
    ws_copy = ws.copy()
    # отсортируем наши параметры wᵢⱼ по возрастанию значения
    ws_copy.sort(key=lambda w: w[1])
    # вернем максимальный по значению wᵢⱼ
    max_ws = []
    # print("ДЕЛЬТЫ")
    for i in ws_copy:
        if i[1] == ws_copy[-1][1]:
            max_ws.append(i)
    print("----------------------------------------")
    print("----МАКСИМАЛЬНЫЕ ДЕЛЬТЫ----")
    print("----------------------------------------")

    for i in max_ws:
        print(i)
    print("----------------------------------------")
    return ws_copy[-1][0], max_ws


def get_possible_next_nodes(cycle, not_visited):
    # возвращает возможные следующие узлы для данного цикла
    last_node = cycle[-1]
    # возможные узлы в строке (если их ещё не посещали и они стоят в той же строке, что и последний узел)
    nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
    # возможные узлы в колонках (если их ещё не посещали и они стоят в той же колонке, что и последний узел)
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]

    if len(cycle) < 2: # если в цикле один узел добавляем оба в возможные направления пересчета
        return nodes_in_row + nodes_in_column
    else:
        prev_node = cycle[-2]
        row_move = prev_node[0] == last_node[0]
        # если мы уже двигались по строке
        if row_move:
            # то возвращаем возможные направления по колонке
            return nodes_in_column
        # если нет, то двигаемся по строке
        return nodes_in_row


def get_cycle(bv_positions, ev_position, bfs):
    print("\n----------------------------------------")
    print("Построим цикл")
    print("----------------------------------------")
    def inner(cycle):
        if len(cycle) > 3:
            print("Цикл длиной больше ТРЕХ, проверяем, можем ли закрыть")
            # если у цикла длина больше 3х, то проверяем, можем ли закрыть

            # если остается только одно возможное направление, то закрываем цикл
            can_be_closed = len(get_possible_next_nodes(cycle, [ev_position])) == 1
            if can_be_closed:
                # возвращаем цикл
                return cycle

        # выбираем все непосещенные ячейки из допустимого базисного решения
        not_visited = list(set(bv_positions) - set(cycle))
        print("Непосещенные клетки из допустимого базиса: ", not_visited)
        # среди непосещенных найдем новое направление для продолжения цикла
        possible_next_nodes = get_possible_next_nodes(cycle, not_visited)
        print("   направление для продолжения цикла: ", possible_next_nodes)


        fig, ax = plt.subplots()
        ax.set_title('Транспортная таблица')

        A = ['A1', 'A2', 'A3', 'A4']
        B = ['B1', 'B2', 'B3', 'B4', 'B5']

        # Размеры таблицы
        rows = len(A) + 1  # +1 для строк с названиями городов прибытия
        cols = len(B) + 1
        # print(A,B)

        positions = [(1, 2), (3, 4), (0, 3), (2, 1), (4, 0)]
        # print(len(positions))
        def update(frame):
            ax.clear()
            ax.axis('off')
            # print(str(bfs[0][1]))
            # print([bfs[0][0]])
            # print ([[[str(bfs[k][1]) if (i, j) in [bfs[k][0]] else '' for k in range(len(bfs))] for j in range(1, cols)] for i in
            #               range(1, rows)])
            cells = ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']
            for k in range(len(bfs)):
                cells[bfs[k][0][0]][bfs[k][0][1]] = str(bfs[k][1])
            print(cells)
            ax.table(
                # cellText=[[[str(bfs[k][1]) if (i, j) in [bfs[k][0]] else '' for k in range(len(bfs))] for j in range(1, cols)] for i in
                #           range(1, rows)],
                # cellText = [['', '', '20', '', ''], ['', '', '', '6', ''], ['', '', '', '', '4'], ['', '', '', '', '']],
                # cellText=[[str(frame + 1) if (i, j) in positions[:frame + 1] else '' for j in range(1, cols)] for i in
                #            range(1, rows)],
                cellText=cells,
                colLabels=B, rowLabels=A, loc='center')
                # cellColours=[['red' if (i, j) in [ev_position] else 'white' for j in range(cols - 1)]
                #                 for i in range(rows - 1)])
                # cellColours=[['red' if (i + 1, j + 1) in positions[:frame + 1] else 'white' for j in range(cols - 1)]
                #              for i in range(rows - 1)])

        ani = FuncAnimation(fig, update, interval=1000)
        plt.show()

        # обход в глубину
        # строим цикл для каждого возможного нового направления
        # print("Обход в глубину: строим цикл для каждого возможного нового направления")
        for next_node in possible_next_nodes:
            print("Переходим к узлу: ", next_node)
            # новый цикл созданный рекурсивно
            new_cycle = inner(cycle + [next_node])
            print("Цикл: ", new_cycle)
            if new_cycle:
                return new_cycle


    return inner([ev_position])



def cycle_pivoting(bfs, cycle):
    # берем четные ячейки из цикла
    even_cells = cycle[0::2]
    # берем нечетные ячейки из цикла
    odd_cells = cycle[1::2]

    # найдем наименьшую нечетную ячейку, которая будет исключена из базиса
    get_bv = lambda pos: next(v for p, v in bfs if p == pos)
    leaving_position = sorted(odd_cells, key=get_bv)[0]
    leaving_value = get_bv(leaving_position)

    new_bfs = []
    # проходимся по всему базисному решению, кроме исключенной ячейки
    for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(cycle[0], 0)]:
        if p in even_cells:
            v += leaving_value
        elif p in odd_cells:
            v -= leaving_value
        # создаем новый базис на основе предыдущего,
        # без исключенной ячейки + параметр wᵢⱼ - начало цикла
        new_bfs.append((p, v))

    return new_bfs


def transportation_simplex_method(supply, demand, costs):
    step = 0

    def inner(bfs, step):
        # вычислим потенциалы потребителя и поставщика для основных переменных -
        # путем ввода новых переменных u и v по соотнощениям:
        # u₁ = 0, uᵢ + vⱼ = cᵢⱼ
        print("bfs: \n", bfs)
        us, vs = get_us_and_vs(bfs, costs, step)
        # для свободных переменных введем параметр w:
        # wᵢⱼ = uᵢ + vⱼ - cᵢⱼ
        ws = get_ws(bfs, costs, us, vs)

        print("----------------------------------------")
        print("----ДЕЛЬТЫ на ", step, " шаге----")
        print("----------------------------------------")
        for w_ in ws:
            print("Ячейка: ", w_[0], "  Значение: ", w_[1])
        print("----------------------------------------")
        # проверка на оптимальность
        # если wᵢⱼ ≤ 0, то базисное решение оптимально
        if can_be_improved(ws):
            # найдем ячейку, для которой будет максимально значение wᵢⱼ = uᵢ + vⱼ - cᵢⱼ
            ev_position, max_ws = get_entering_variable_position(ws)
            print("Начало цикла:  ", ev_position)
            # найдем цикл для заданного списка
            # с позициями основных переменных и позицией входящей переменной
            cycle = get_cycle([p for p, v in bfs], ev_position, bfs)
            print("Получили готовый цикл")
            print("\nДопустимое базисное решение:")
            print_bfs(bfs, len(costs), len(costs[0]))
            print("\nЦикл:")
            print_cycle(ev_position, cycle, bfs, len(costs), len(costs[0]))

            # рекурсивно улучшаем наше решение
            return inner(cycle_pivoting(bfs, cycle), step+1)

        print("\nРешение:")
        print_bfs(bfs, len(costs), len(costs[0]))
        return bfs

    # находим начальное базисное решение методом северо-западного угла
    basic_feasible_sol = north_west_corner(supply, demand)
    print("\nБазис, полученный методом северо-западного угла:")
    print_bfs(basic_feasible_sol, len(costs), len(costs[0]))

    # решаем задачу методом потенциалов
    basic_variables = inner(basic_feasible_sol, 1)

    solution = np.zeros((len(costs), len(costs[0])))
    for (i, j), v in basic_variables:
        solution[i][j] = v

    return solution