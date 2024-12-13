def print_problem(supply, demand, costs):
    print("Предложение:")
    print(supply)
    print("Спрос:")
    print(demand)
    print("Стоимость перевозок:")
    for i in range(len(costs)):
        print(costs[i])
    print()

def print_cycle(start_pos, cycle, bfs, len_col, len_row):
    cycle_table = [['0' for j in range(len_row)] for i in range(len_col)]
    ctr = 1
    cycle_table[start_pos[0]][start_pos[1]] = "*_0"
    for (i, j), v in bfs:
        if (i, j) in cycle:
            if ctr == 1:
                cycle_table[i][j] = str(v) + "_" + str(ctr)
                ctr = len(cycle) - 1
            else:
                cycle_table[i][j] = str(v) + "_" + str(ctr)
                ctr -= 1


    for row in cycle_table:
        print(row)
    print()

def print_bfs(bfs, len_col, len_row):
    bfs_table = [['0' for j in range(len_row)] for i in range(len_col)]
    for (i, j), v in bfs:
        bfs_table[i][j] = str(v) + "_b"

    for row in bfs_table:
        print(row)


def print_solution_tp(costs, solution):
    print()
    # рассчитываем итоговую стоимость
    total_cost = 0
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            if solution[i][j] != 0:
                print("Из " + str(i + 1) + "-го склада нужно доставить в "
                  + str(j + 1) + "-й магазин " + str(solution[i][j])
                  + " ед. товара, стоимость: " + str(cost * solution[i][j]) )
            total_cost += cost * solution[i][j]
    print("Итого, минимальные затраты составят: " + str(total_cost))
    return total_cost