import numpy as np
from brute_force import solve_brute_force
from canon import to_canon
from closing import make_closed_tp
from input import input_
from prints import print_solution_tp, print_problem, print_table
from transport_simplex import transportation_simplex_method


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def main():
    supply, demand, costs = input_("input.txt")
    print("\n----------------------------------------")
    print("\n----ИСХОДНАЯ ТРАНСПОРТНАЯ ЗАДАЧА----")
    print("\n----------------------------------------")
    print_problem(supply, demand, costs)

    # приводим задачу в закрытую форму
    closed_supply, closed_demand, closed_costs = make_closed_tp(supply, demand, costs)

    solution = transportation_simplex_method(closed_supply, closed_demand, closed_costs)

    print_solution_tp(costs, solution)

    print("\n----------------------------------------")
    print("\n----МЕТОД ПЕРЕБОРА КРАЙНИХ ТОЧЕК----")
    print("\n----------------------------------------")
    min_task, A_matr, b_vec = to_canon(len(closed_supply), len(closed_demand), closed_supply, closed_demand,
                                       closed_costs)
    # удалить последнюю строчку
    A_matr.pop(len(A_matr) - 1)
    b_vec.pop(len(b_vec) - 1)
    brute_solution = solve_brute_force(A_matr, b_vec, min_task, 0)
    brute_solution = np.reshape(brute_solution, (len(closed_supply), len(closed_demand)))
    print_table(brute_solution, headers=[])

    print_solution_tp(costs, brute_solution)


main()
