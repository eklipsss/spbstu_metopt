def input_(filename: str):
    with open(filename, 'r') as fp:
        str = fp.readline()
        A_list = str.split(' ')
        A_list = [int(x) for x in A_list]
        str = fp.readline()
        B_list = str.split(' ')
        B_list = [int(x) for x in B_list]
        C_list = []
        for n, line in enumerate(fp, 1):
            str = line.rstrip('\n')
            if (str[0] == 'N' or str[0] == 'Y'):fuf
                continue
            arr = str.split(' ')
            arr = [int(x) for x in arr]
            C_list.append(arr)
        #
        # # штрафы за неудовлетворение спроса
        # penalties_for_more_demand = [0, 0, 0, 0, 0]
        # # штрафы за непокрытие предложения
        # penalties_for_more_supply = [0, 0, 0, 0]
        #
        # str = fp.readline()
        # if str == "Y":
        #     str = fp.readline()
        #     penalties_for_more_demand = str.split(' ')
        #     penalties_for_more_demand = [int(x) for x in penalties_for_more_demand]
        #     str = fp.readline()
        #     penalties_for_more_supply = str.split(' ')
        #     penalties_for_more_supply = [int(x) for x in penalties_for_more_supply]


        return A_list, B_list, C_list