# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
#
# def display_transport_table(rows, cols, positions, departure_cities, destination_cities):
#     # Функция для отображения таблицы с закрашенными ячейками
#
#     # Создание пустой таблицы
#     table = [[' ' for _ in range(cols)] for _ in range(rows)]
#
#     # Закрашивание ячеек согласно позициям
#     for i, pos in enumerate(positions):
#         row, col = pos
#         table[row][col] = str(i+1)  # Индекс позиции
#
#     # Установка названий городов отправления
#     for i, city in enumerate(departure_cities):
#         table[i+1][0] = city
#
#     # Установка названий городов прибытия
#     for i, city in enumerate(destination_cities):
#         table[0][i+1] = city
#
#     # Вывод таблицы
#     for row in table:
#         print('|'.join(row))
#
# def animate_transport_table(rows, cols, positions, departure_cities, destination_cities):
#     # Функция для анимации таблицы с закрашенными ячейками
#     fig, ax = plt.subplots()
#     ax.set_title('Транспортная таблица')
#
#     def update(frame):
#         ax.clear()
#         ax.axis('off')
#         ax.table(cellText=[[str(frame+1) if (i, j) in positions[:frame+1] else '' for j in range(1, cols)] for i in range(1, rows)],
#                  colLabels=destination_cities, rowLabels=departure_cities, loc='center')
#
#     ani = FuncAnimation(fig, update, frames=len(positions), interval=1000)
#     plt.show()
#
# def main():
#     # Названия городов отправления и прибытия
#     departure_cities = ['A1', 'A2', 'A3', 'A4']
#     destination_cities = ['B1', 'B2', 'B3', 'B4', 'B5']
#
#     # Размеры таблицы
#     rows = len(departure_cities) + 1  # +1 для строк с названиями городов прибытия
#     cols = len(destination_cities) + 1  # +1 для столбцов с названиями городов отправления
#
#     # Пример массива позиций (ячейки, которые нужно закрасить)
#     positions = [(1, 2), (3, 4), (0, 3), (2, 1), (4, 0)]  # формат (строка, столбец)
#
#     # Вывод статической таблицы
#     print("Статическая таблица для транспортной задачи:")
#     display_transport_table(rows, cols, positions, departure_cities, destination_cities)
#
#     # Анимация таблицы
#     print("\nАнимация транспортной таблицы:")
#     animate_transport_table(rows, cols, positions, departure_cities, destination_cities)
#
# if __name__ == "__main__":
#     main()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#
# def display_transport_table(rows, cols, positions, departure_cities, destination_cities):
#     # Функция для отображения таблицы с закрашенными ячейками
#
#     # Создание пустой таблицы
#     table = [[' ' for _ in range(cols)] for _ in range(rows)]
#
#     # Закрашивание ячеек согласно позициям
#     for i, pos in enumerate(positions):
#         row, col = pos
#         table[row][col] = str(i + 1)  # Индекс позиции
#
#     # Установка названий городов отправления
#     for i, city in enumerate(departure_cities):
#         table[i + 1][0] = city
#
#     # Установка названий городов прибытия
#     for i, city in enumerate(destination_cities):
#         table[0][i + 1] = city
#
#     # Вывод таблицы с цветами
#     for i in range(rows):
#         for j in range(cols):
#             if (i, j) in positions:
#                 plt.text(j, i, table[i][j], ha='center', va='center', color='red', fontsize=12)
#             else:
#                 plt.text(j, i, table[i][j], ha='center', va='center', fontsize=12)
#     plt.xticks([])
#     plt.yticks([])
#     plt.show()


def animate_transport_table(rows, cols, positions, departure_cities, destination_cities):
    # Функция для анимации таблицы с закрашенными ячейками
    fig, ax = plt.subplots()
    ax.set_title('Транспортная таблица')

    def update(frame):
        ax.clear()
        ax.axis('off')
        print(positions[:frame + 1])
        print(str(frame + 1))
        ax.table(cellText=[[str(frame + 1) if (i, j) in positions[:frame + 1] else '' for j in range(1, cols)] for i in
                           range(1, rows)],
                 colLabels=destination_cities, rowLabels=departure_cities, loc='center',
                 cellColours=[['red' if (i + 1, j + 1) in positions[:frame + 1] else 'white' for j in range(cols - 1)]
                              for i in range(rows - 1)])

    ani = FuncAnimation(fig, update, frames=len(positions), interval=1000)
    plt.show()


def main():
    # Названия городов отправления и прибытия
    A = ['A1', 'A2', 'A3', 'A4']
    B = ['B1', 'B2', 'B3', 'B4', 'B5']

    # Размеры таблицы
    rows = len(A) + 1  # +1 для строк с названиями городов прибытия
    cols = len(B) + 1  # +1 для столбцов с названиями городов отправления

    # Пример массива позиций (ячейки, которые нужно закрасить)
    positions = [(1, 2), (3, 4), (0, 3), (2, 1), (4, 0)]  # формат (строка, столбец)

    # # Вывод статической таблицы
    # print("Статическая таблица для транспортной задачи:")
    # display_transport_table(rows, cols, positions, A, B)

    # Анимация таблицы
    print("\nАнимация транспортной таблицы:")
    animate_transport_table(rows, cols, positions, A, B)


if __name__ == "__main__":
    main()
