def north_west_corner(supply, demand):
    # копируем вектора предложения и спроса
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    i = 0
    j = 0

    # создаем новый массив
    # будет хранить в себе индексы и значения для базисного допустимого решения
    bfs = []

    while len(bfs) < len(supply) + len(demand) - 1:
        # берем остаток из предложения
        s = supply_copy[i]
        # берем остаток от спроса
        d = demand_copy[j]
        # находим минимум среди них
        v = min(s, d)

        # вычитаем найденный минимум из предложения и спроса
        supply_copy[i] -= v
        demand_copy[j] -= v

        # добавляем индексы и значения для базисного допустимого решения
        bfs.append(((i, j), v))

        if supply_copy[i] == 0 and i < len(supply) - 1:
            # если минимумом оказалось предложение, передвигаемся вниз
            i += 1
        elif demand_copy[j] == 0 and j < len(demand) - 1:
            # если минимумом оказался спрос, передвигаемся вправо
            j += 1
    return bfs