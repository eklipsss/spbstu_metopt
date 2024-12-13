from tabulate import tabulate

def print_table(matrix, headers):
    print(tabulate(matrix, headers, tablefmt="rounded_grid"))
def print_problem(supply, demand, costs):
    print("Количество груза в пунктах хранения:  ", supply)
    # print(supply)
    print("Потребность в грузе в пунктах назначения:  ", demand)
    # print(demand)
    print("Матрица тарифов:")
    print_table(costs, headers=[])
    # for i in range(len(costs)):
    #     print(costs[i])
    print()


def print_cycle(start_pos, cycle, bfs, len_col, len_row):
    cycle_table = [['0' for j in range(len_row)] for i in range(len_col)]
    ctr = 1
    cycle_table[start_pos[0]][start_pos[1]] = "*_0"
    for (i, j), v in bfs:
        if (i, j) in cycle:
            cycle_table[i][j] = str(v) + "_" + str(ctr)
            ctr+=1
    print_table(cycle_table, headers=[])
    # for row in cycle_table:
    #     print(row)
    print()

def print_full_cycle(start_pos, cycle, bfs, len_col, len_row):
    cycle_full_table = [['0' for j in range(len_row)] for i in range(len_col)]
    ctr = 1
    cycle_full_table[start_pos[0]][start_pos[1]] = "*_0"
    for (i, j), v in bfs:
        cycle_full_table[i][j] = str(v) + "_" + str(ctr)
        ctr+=1

    print_table(cycle_full_table, headers=[])
    print()



def print_bfs(bfs, len_col, len_row):
    bfs_table = [['0' for j in range(len_row)] for i in range(len_col)]
    for (i, j), v in bfs:
        bfs_table[i][j] = str(v) + "_b"

    print_table(bfs_table, headers=[])

    # for row in bfs_table:
    #     print(row)


def print_solution_tp(costs, solution):
    print()
    # рассчитываем итоговую стоимость
    total_cost = 0
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            if solution[i][j] != 0:
                print("От " + str(i + 1) + "-го поставщика нужно доставить "
                  + str(j + 1) + "-ому потребителю " + str(solution[i][j])
                  + " ед. товара, общей стоимостью: " + str(cost * solution[i][j]))
                print("Стоимость: ", cost, " Объем: ", solution[i][j])
            total_cost += cost * solution[i][j]
    print("Итого, минимальные затраты составят: " + str(total_cost))
    return total_cost