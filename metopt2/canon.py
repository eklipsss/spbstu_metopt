def to_canon(M : int, N : int, m_count : list, n_count : list, coefs : list):
    min_task = list()
    for i in range(M):
        for j in range(N):
            min_task.append(int(coefs[i][j]))

    b_vec = [m_count[i] if i < M else n_count[i - M] for i in range(M + N)]
    A_matr = [[0 for i in range(M * N)] for i in range (M + N)]

    # заполняем строки-ограничения на поставку
    for i in range(M):
        for j in range(N):
            A_matr[i][i * N + j] = 1

    # заполняем строки-ограничения на прием
    for i in range(N):
        for j in range(M):
            A_matr[M + i][i + j * N] = 1

    return min_task, A_matr, b_vec