import copy
import random
DEBUG = True
CHECK_FOR_DEGENERATE = True

inf = float('Inf')

def print_matr(matr, system_of_nulls = None, quouted_zeros = None):
    if system_of_nulls == None:
        system_of_nulls = []
    for i in range(0, len(matr)):
        for j in range(0, len(matr[0])):
            if matr[i][j] == 0 and ((i, j) in system_of_nulls):
                print('*', end=' ')
            if (quouted_zeros is not None) and matr[i][j] == 0 and ((i, j) in quouted_zeros):
                print('\'', end=' ')
            else:
                print(matr[i][j], end=' ')
        print()
    print()

def debug_print(outp, system_of_nulls = None, quoted_zeros = None):
    if DEBUG:
        if isinstance(outp, str):
            print(outp)
        else:
            print_matr(outp, system_of_nulls, quoted_zeros)

def northern_west_method(needs, stocks):
    needs = needs[:]
    stocks = stocks[:]
    results = [[0 for j in range(0, len(needs))] for i in range(0, len(stocks))]

    for i in range(0, len(stocks)):
        for j in range(0, len(needs)):
            to_transport = stocks[i] if stocks[i] <= needs[j] else needs[j]
            results[i][j] += to_transport
            stocks[i] -= to_transport
            needs[j] -= to_transport

    return results

def check_distributions(needs, stocks, distribution):
    for i in range(0, len(stocks)):
        total_needs = 0
        for j in range(0, len(needs)):
            total_needs += distribution[i][j]
        assert total_needs == stocks[i], 'error in distribution'

    for j in range(0, len(needs)):
        total_stocks = 0
        for i in range(0, len(stocks)):
            total_stocks += distribution[i][j]
        assert total_stocks == needs[j], 'error in distribution'

def get_cost(prices, distribution):
    total_cost = 0
    for i in range(0, len(prices)):
        for j in range(0, len(prices[0])):
            total_cost += prices[i][j] * distribution[i][j]
    return total_cost

def check_degenerate(distribution, basis_nodes):
    if not CHECK_FOR_DEGENERATE:
        return False
    return len(distribution) + len(distribution[0]) - 1 > len(basis_nodes)

def get_basis_nodes(distribution):
    basis_nodes = []
    for i in range(0, len(distribution)):
        for j in range(0, len(distribution[0])):
            if distribution[i][j] != 0:
                basis_nodes.append((i, j))
    if not check_degenerate(distribution, basis_nodes):
        return set(basis_nodes)

    all_possible_nodes = set([(i, j) for j in range(0, len(distribution[0])) for i in range(0, len(distribution))])
    non_basis_nodes = all_possible_nodes - set(basis_nodes)
    random_elements = random.sample(list(non_basis_nodes), len(distribution) + len(distribution[0]) - 1 - len(basis_nodes))
    basis_nodes.extend(random_elements)
    return set(basis_nodes)

def calc_potentials_row(stocks_potential, needs_potential, prices, basis_nodes, column_num):
    for i in range(0, len(stocks_potential)):
        if ((i, column_num) in basis_nodes) and (stocks_potential[i] == inf):
            stocks_potential[i] = prices[i][column_num] - needs_potential[column_num]
            calc_potentials_column(stocks_potential, needs_potential, prices, basis_nodes, i)

def calc_potentials_column(stocks_potential, needs_potential, prices, basis_nodes, row_num):
    for j in range(0, len(needs_potential)):
        if ((row_num, j) in basis_nodes) and (needs_potential[j] == inf):
            needs_potential[j] = prices[row_num][j] - stocks_potential[row_num]
            calc_potentials_row(stocks_potential, needs_potential, prices, basis_nodes, j)

def calc_potentials(prices, basis_nodes):
    stocks_potentials = [inf for i in range(0, len(prices))]
    needs_potentials = [inf for i in range(0, len(prices[0]))]
    stocks_potentials[0] = 0
    calc_potentials_column(stocks_potentials, needs_potentials, prices, basis_nodes, 0)
    return stocks_potentials, needs_potentials

def get_min_delta_ind(prices, stocks_potentials, needs_potentials, basis_nodes):
    deltas = copy.deepcopy(prices)
    min_value = 0
    min_ind = None
    for i in range(0, len(deltas)):
        for j in range(0, len(deltas[0])):
            if (i, j) in basis_nodes:
                deltas[i][j] = 0
            else:
                deltas[i][j] -= stocks_potentials[i] + needs_potentials[j]
            if deltas[i][j] < 0:
                if deltas[i][j] < min_value:
                    min_value = deltas[i][j]
                    min_ind = (i, j)
    return min_ind

def create_cycle_column(prices, basis_nodes, start_point, cycle, column_num):
    for i in range(0, len(prices)):
        if ((i, column_num) in basis_nodes) and ((i, column_num) not in cycle):
            cycle.append((i, column_num))
            create_cycle_row(prices, basis_nodes, start_point, cycle, i)
            break

def create_cycle_row(prices, basis_nodes, start_point, cycle, row_num):
    if row_num == start_point[0]:
        return
    for j in range(0, len(prices[0])):
        if ((row_num, j) in basis_nodes) and ((row_num, j) not in cycle):
            cycle.append((row_num, j))
            create_cycle_column(prices, basis_nodes, start_point, cycle, j)
            break

def create_cycle(price, basis_nodes, start_point):
    cycle = [start_point]
    create_cycle_column(price, basis_nodes, start_point, cycle, start_point[1])
    return cycle

def remake_distibution(distribution, cycle):
    value_cycle = [distribution[elem[0]][elem[1]] for elem in cycle]
    min_value = min(value_cycle[1::2])
    positive = True
    for elem in cycle:
        if positive:
            distribution[elem[0]][elem[1]] += min_value
            positive = False
        else:
            distribution[elem[0]][elem[1]] -= min_value
            positive = True

def transport_task_solver(prices, needs, stocks):
    distribution = northern_west_method(needs, stocks)
    check_distributions(needs, stocks, distribution)
    debug_print('Transport table after norther-west method:')
    debug_print(distribution)

    iter = 1
    while True:
        debug_print("Iteration %d:" % iter)
        potential_counted = False
        optimized = False
        while not potential_counted:
            basis_nodes = get_basis_nodes(distribution)
            (stocks_potentials, needs_potentials) = calc_potentials(prices, basis_nodes)
            potential_counted = True
            for potential in stocks_potentials:
                if potential == inf:
                    potential_counted = False
                    break
            for potential in needs_potentials:
                if potential == inf:
                    potential_counted = False
                    break
            min_ind = get_min_delta_ind(prices, stocks_potentials, needs_potentials, basis_nodes)
            if min_ind is None:
                optimized = True
                break
            cycle = create_cycle(prices, basis_nodes, min_ind)
            if (len(cycle) <= 2) or (cycle[0][0] != cycle[len(cycle) - 1][0]):
                potential_counted = False
        if optimized:
            break
        debug_print('Cycle: %s' % str(cycle))
        remake_distibution(distribution, cycle)
        debug_print('Current transport table')
        debug_print(distribution)
        check_distributions(needs, stocks, distribution)
        current_price = get_cost(prices, distribution)
        debug_print('Current price: %d' % current_price)
        iter = iter + 1
    final_price = get_cost(prices, distribution)
    print('Final price: %d' % final_price)
    return final_price

#part 1
needs = [40, 30, 85, 40]
stocks = [55, 95, 45]
prices = [[7, 0, 8, 6], [3, 5, 1, 11], [2, 4, 7, 8]]

#part 2
#prices = [[6, 10, 4, 5, 8], [8, 10, 7, 9, 11], [4, 8, 9, 10, 6], [5, 9, 6, 11, 10], [6, 11, 6, 3, 9]]
#stocks = [1, 1, 1, 1, 1]
#needs = [1, 1, 1, 1, 1]

if __name__ == '__main__':
    transport_task_solver(prices, needs, stocks)