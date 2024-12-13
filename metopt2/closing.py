# функция перевода транспортной задачи в закрытую форму
from prints import print_problem


def make_closed_tp(supply, demand, costs):
    print("Алгоритм приведения задачи к закрытому виду...")
    # всего предложения
    total_supply = sum(supply)

    # всего спроса
    total_demand = sum(demand)

    print("Общее количество груза в пунктах хранения:")
    print(total_supply)
    print("Общая потребность в грузе в пунктах назначения:")
    print(total_demand)

    # если спроса больше, то вводим штрафы за неустойку
    if total_supply < total_demand:
        print("Недопоставка:")
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [[0]*5]
        print_problem(new_supply, demand, new_costs)
        return new_supply, demand, new_costs

    # если
    if total_supply > total_demand:
        print("Избыточность хранения:")
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs
        for i in range(len(new_costs)):
            new_costs[i].append(0)

        print_problem(supply, new_demand, new_costs)
        return supply, new_demand, new_costs
    print("Задача имеет закрытый вид \n")
    return supply, demand, costs