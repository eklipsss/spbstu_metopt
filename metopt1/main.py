import copy  # для создания глубоких копий списков
import numpy as np
from itertools import \
    combinations  # возвращает итератор со всеми возможными комбинациями элементов входной последовательности iterable.
# Каждая комбинация заключена в кортеж с длинной r элементов, в которой нет повторяющихся элементов.
from simplex import simplex
from simplex2 import simplex_method, canonization

# from simplex import transportation_simplex_method
"""
Чтение файла. Сохраняем систему.
Предполагается, что в строке, начинающейся с goal_gunc, записана целевая функция.
В строке, начинающейся с idx, записаны индексы переменных, имеющих ограничение на знак >= 0.
"""


def read_file(filename):
    matrix = []
    sign = []
    goal_func = []
    idx = []
    with open(filename, "r") as f:
        for line in f.readlines():
            expression = line.split()
            if expression[0] == "goal_func":
                expression.remove("goal_func")
                for value in expression:
                    goal_func.append(float(value))
                continue
            if expression[0] == "idx":
                expression.remove("idx")
                for value in expression:
                    idx.append(int(value))
                continue
            coeffs = []
            for value in expression:
                if value.isdigit() or value[0] == '-':
                    coeffs.append(float(value))
                else:
                    sign.append(value)
            matrix.append(coeffs)
    return matrix, sign, goal_func, idx

def first_step(matrix, sign):
    for i in range(len(sign)):
        if sign[i]=="<=":
            sign[i]=">="
            for j in range(len(matrix[i])):
                matrix[i][j]*=-1
        # print(matrix[i])
    return matrix, sign


def to_canonical(matrix, sign, goal_func, idx):
    # копирование данных, чтобы исходные остались прежними
    copy_sign = copy.deepcopy(sign)
    copy_matrix = copy.deepcopy(matrix)
    copy_idx = copy.deepcopy(idx)
    copy_goal_func = copy.deepcopy(goal_func)
    # приводим к канонической форме
    # сначала заменяем все знаки на равенства
    for i in range(len(copy_matrix)):
        if copy_sign[i] == '<=':  # если знак <=
            for j in range(len(copy_matrix)):
                if j == i:
                    copy_matrix[j].insert(-1, 1.0)  # добавляем новую переменную со коэф-том 1
                    copy_idx.append(len(copy_matrix[j]) - 2)  # у переменной ограничение на знак
                else:
                    copy_matrix[j].insert(-1, 0.0)
            copy_goal_func.append(0.0)
            copy_sign[i] = '='  # делаем равенство
        if copy_sign[i] == '>=':  # если знак >=
            for j in range(len(copy_matrix)):
                if j == i:
                    copy_matrix[j].insert(-1, -1.0)  # добавляем новую переменную со коэф-том -1
                    copy_idx.append(len(copy_matrix[j]) - 2)
                else:
                    copy_matrix[j].insert(-1, 0.0)
            copy_goal_func.append(0.0)
            copy_sign[i] = '='
    # теперь переменные без ограничения на знак заменяем новыми
    # в том числе в ф-ии цели
    to_delete = []  # здесь будем хранить индексы "старых" переменных
    for i in range(len(copy_matrix[0]) - 1):
        if ((i+1) not in copy_idx) and (i!=len(copy_matrix[0]) - 2):
        # if ((i + 1) not in copy_idx):
            # значит на знак нет ограничения
            for j in range(len(copy_matrix)):
                # заменяем переменную без ограничения на u-v (разницу двух новых переменных)
                copy_matrix[j].insert(-1, copy_matrix[j][i])
                copy_matrix[j].insert(-1, -copy_matrix[j][i])
            copy_goal_func.insert(-1, copy_goal_func[i])
            copy_goal_func.insert(-1, -copy_goal_func[i])
            to_delete.append(i)
    to_delete = to_delete[::-1]
    for i in range(len(copy_matrix)):
        for j in to_delete:
            copy_matrix[i].pop(j)
    for j in to_delete:
        copy_goal_func.pop(j)
    copy_idx = [(i+1) for i in range(len(copy_matrix[0]) - 1)]
    return copy_matrix, copy_sign, copy_goal_func, copy_idx

def canonical_positive(matrix):
    for i in range(len(matrix)):
        if matrix[i][-1]<0:
            for j in range(len(matrix[i])):
                matrix[i][j]*=-1
    return matrix


def direct_to_dual(matrix, sign, goal_func, idx):
    dual_goal_func = []
    dual_idx = []
    dual_sign = []
    for vect in matrix:
        dual_goal_func.append(vect[-1])

    # создаем двойственную систему
    dual_matrix = list(map(list, zip(*matrix)))  # транспонированная матрица
    # for i in dual_matrix:
    #     print(i)
    dual_matrix.pop(-1)

    for i in range(len(dual_matrix)):
        dual_matrix[i].append(goal_func[i])  # добавляем свободные члены
        # print("dual_matrix[i]", dual_matrix[i])
        # print('sign', sign, '\n')
        if (i+1) in idx:  # и смотрим знаки новой системы: если на i было ограничение
            dual_sign.append('<=')  # то знак <=
        else:
            dual_sign.append('=')  # иначе =
    for i in range(len(sign)):
        if sign[i] == '>=':
            dual_idx.append(i+1)
        if sign[i] == '<=':
            dual_idx.append(-i-1)  # если idx отрицательный, значит x[i] <= 0, если idx положит, то x[i] >= 0
    for i in range(len(dual_idx)):
        if dual_idx[i]<0:
            for j in range(len(dual_matrix)):
                # print("[j][abs(i)-1] = [", j, "], [", abs(i), "], dual_matrix[j][abs(i)-1] ", dual_matrix[j][abs(i)-1])
                dual_matrix[j][abs(dual_idx[i])-1]*=-1
            # print("dual_goal_func[abs(i)-1] ", dual_goal_func[abs(i)-1])
            dual_goal_func[abs(dual_idx[i])-1]*=-1
            dual_idx[i]*=-1
    # for i in dual_matrix:
    #     print(i)
    return dual_matrix, dual_sign, dual_goal_func, dual_idx


EPS = 0.000000001


def get_basis_matrs(A: np.ndarray):
    N = A.shape[0]  # строки
    M = A.shape[1]  # столбцы

    basis_matrs = []
    basis_combinations_indexes = []
    all_indexes = [i for i in range(M)]

    for i in combinations(all_indexes, N):
        basis_matr = A[:, i]
        if np.linalg.det(basis_matr) != 0:  # проверяем, что определитель отличен от нуля
            basis_matrs.append(basis_matr)  # получаем все такие матрицы и индексы комбинаций записываем
            basis_combinations_indexes.append(i)

    print("Количество базисных матриц: ", len(basis_matrs))

    return basis_matrs, basis_combinations_indexes


def get_all_possible_vectors(A: list, b: list):
    N = len(A[0])
    M = len(A)
    vectors = []

    if M >= N:  # Рассматривается матрица A[M,N}, где число строк меньше числа столбцов (M < N)
        return vectors  # пустой список - так как система линейных уравнений не имеет решений
    else:
        basis_matrs, basis_combinations_indexes = get_basis_matrs(np.array(A))

    for i in range(len(basis_matrs)):  # Для всех матриц с ненулевым определителем
        solve = np.linalg.solve(basis_matrs[i], b)  # Решаем систему вида A[M,N_k]*x[N]=b[M] - Метод Гаусса
        if (len(solve[solve < -1 * EPS]) != 0) or (len(solve[solve > 1e+15]) != 0):
            continue

        vec = [0 for i in range(N)]  # заполняем нулями до N
        for j in range(len(basis_combinations_indexes[i])):
            vec[basis_combinations_indexes[i][j]] = solve[j]
        vectors.append(vec)
    return vectors


def solve_brute_force(A: list, b: list, goal_func: list) -> object:
    vectors = get_all_possible_vectors(A, b)  # получаем все возможные опорные вектора
    if len(vectors) == 0:  # если их нет, нет оптимального решения
        return []

    solution = vectors[0]
    target_min = np.dot(solution, goal_func)

    for vec in vectors:
        if np.dot(vec, goal_func) < target_min:  # находим минимум
            target_min = np.dot(vec, goal_func)  # значение функции цели в крайней точке
            solution = vec

    print("Лучшее значение целевой функции: ", target_min)

    return solution


""" Вспомогательная ф-я для получения отдельной матрицы A и вектора b из matrix """


def getAb(matrix):
    A = []
    b = []
    for vec in matrix:
        b.append(vec[-1])
        A.append(vec[:-1])
    return A, b


def print_system(matrix, sign, goal_func, idx):
    A, b = getAb(matrix)
    for i in range(len(A)):
        for j in range(len(A[i])):
            if (A[i][j] == 0):
                continue
            print(A[i][j], '*x[', j, ']', end='', sep='')
            if j != len(A[i]) - 1:
                print(' + ', end='')
        print(' ', sign[i], b[i], sep=' ')
    print('Целевая функция: ', goal_func)
    print('Индексы переменных с ограничением на знак: ', idx)
    print('\n')

def reverse_sign(goal_func):
    return [-i for i in goal_func]


matrix, sign, goal_func, idx = read_file("task2.txt")
# matrix, sign, goal_func, idx = read_file("task.txt")

print('\n\n---ПРЯМАЯ ЗАДАЧА---')
print('------ min ------')
print_system(matrix, sign, goal_func, idx)

print('---ПРЯМАЯ ЗАДАЧА - ПЕРВОЕ ПРЕОБРАЗОВАНИЕ (ЗНАКИ)---')
print('------ min ------')
matrix_f, sign_f = first_step(matrix, sign)
print_system(matrix_f, sign_f, goal_func, idx)

print('---КАНОНИЧЕСКАЯ ФОРМА ПРЯМОЙ ЗАДАЧИ---')
print('------ min ------')
matrix_c_dir, sign_c_dir, goal_func_c_dir, idx_c_dir = to_canonical(matrix_f, sign_f, goal_func, idx)
print_system(matrix_c_dir, sign_c_dir, goal_func_c_dir, idx_c_dir)

print('---КАНОНИЧЕСКАЯ ФОРМА ПРЯМОЙ ЗАДАЧИ - ПОЛОЖИТЕЛЬНЫЕ СВОБОДНЫЕ ЧЛЕНЫ---')
print('------ min ------')
matrix_c_dir_p = canonical_positive(matrix_c_dir)
print_system(matrix_c_dir_p, sign_c_dir, goal_func_c_dir, idx_c_dir)

print('---ДВОЙСТВЕННАЯ ЗАДАЧА---')
print('------ max ------')
matrix_dual, sign_dual, goal_func_dual, idx_dual = direct_to_dual(matrix_f, sign_f, goal_func, idx)
print_system(matrix_dual, sign_dual, goal_func_dual, idx_dual)

print('---ДВОЙСТВЕННАЯ ЗАДАЧА---')
print('------ min ------')
matrix_dual_f, sign_dual_f = first_step(matrix_dual, sign_dual)
goal_func_dual_m = reverse_sign(goal_func_dual)
print_system(matrix_dual_f, sign_dual_f, goal_func_dual_m, idx_dual)

print('---КАНОНИЧЕСКАЯ ФОРМА ДВОЙСТВЕННОЙ ЗАДАЧИ---')
print('------ min ------')
matrix_c_dual, sign_c_dual, goal_func_c_dual, idx_c_dual = to_canonical(matrix_dual_f, sign_dual_f, goal_func_dual_m, idx_dual)
# matrix_c_dual, sign_c_dual, goal_func_c_dual, idx_c_dual = to_canonical(matrix_dual, sign_dual, goal_func_dual, idx_dual)
print_system(matrix_c_dual, sign_c_dual, goal_func_c_dual, idx_c_dual)

print('---КАНОНИЧЕСКАЯ ФОРМА ДВОЙСТВЕННОЙ ЗАДАЧИ - ПОЛОЖИТЕЛЬНЫЕ СВОБОДНЫЕ ЧЛЕНЫ---')
print('------ min ------')
matrix_c_dual_p = canonical_positive(matrix_c_dual)
print_system(matrix_c_dual_p, sign_c_dual, goal_func_c_dual, idx_c_dual)

print('\n---РЕШЕНИЕ ПРЯМОЙ ЗАДАЧИ МЕТОДОМ ПЕРЕБОРА ОПОРНЫХ ВЕКТОРОВ---')
A, b = getAb(matrix_c_dir)
solution = solve_brute_force(A, b, goal_func_c_dir)
print('Вектор решения: ', solution)

# print('\n---РЕШЕНИЕ ДВОЙСТВЕННОЙ ЗАДАЧИ МЕТОДОМ ПЕРЕБОРА ОПОРНЫХ ВЕКТОРОВ---')
# A_dual, b_dual = getAb(matrix_c_dual_p)
# solution_dual = solve_brute_force(A_dual, b_dual, goal_func_c_dual)
# print('Вектор решения: ', solution_dual)
#
print('\n---РЕШЕНИЕ ПРЯМОЙ ЗАДАЧИ СИМПЛЕКС-МЕТОДОМ---')
mat, fun, bas = canonization(A, b, goal_func_c_dir)
simplex_method(mat, fun, bas, True)
# solution = simplex(goal_func_c_dir, A, b)
# solution = transportation_simplex_method(goal_func_c_dir, A, b)
print('Вектор решения: ', solution)

# print('\n---РЕШЕНИЕ ПРЯМОЙ ЗАДАЧИ СИМПЛЕКС-МЕТОДОМ---')
# solution = simplex(goal_func_c_dir, A, b)
# # solution = transportation_simplex_method(goal_func_c_dir, A, b)
# print('Вектор решения: ', solution)
#
# print('\n---РЕШЕНИЕ ДВОЙСТВЕННОЙ ЗАДАЧИ СИМПЛЕКС-МЕТОДОМ---')
# solution_dual = simplex(goal_func_c_dual, A_dual, b_dual)
# # solution_dual = transportation_simplex_method(goal_func_c_dual, A_dual, b_dual)
# print('Вектор решения: ', solution_dual)
