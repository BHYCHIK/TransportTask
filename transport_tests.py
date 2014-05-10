import transport

def check_calc_potentials():
    prices = [[2, 3, 2, 4], [3, 2, 5, 1], [4, 3, 2, 6]]
    basis_nodes = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    (stocks_potentials, needs_potentials) = transport.calc_potentials(prices, basis_nodes)
    if (stocks_potentials == [0, -1, -4]) and (needs_potentials == [2, 3, 6, 10]):
        return True
    else:
        return False

def check_min_delta_ind():
    prices = [[2, 3, 2, 4], [3, 2, 5, 1], [4, 3, 2, 6]]
    basis_nodes = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    stocks_potentials = [0, -1, -4]
    needs_potentials = [2, 3, 6, 10]
    min_ind = transport.get_min_delta_ind(prices, stocks_potentials, needs_potentials, basis_nodes)
    if min_ind == (1, 3):
        return True
    else:
        return False

def check_cycle_builder():
    prices = [[2, 3, 2, 4], [3, 2, 5, 1], [4, 3, 2, 6]]
    basis_nodes = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    min_ind = (1, 3)
    cycle = transport.create_cycle(prices, basis_nodes, min_ind)
    if cycle == [(1, 3), (2, 3), (2, 2), (1, 2)]:
        return True
    else:
        return False

def run_tests():
    if check_calc_potentials():
        print('Checking potentials works ok!')
    else:
        print('Checking potentials not work ok!')

    if check_min_delta_ind():
        print('Checking min deltas works ok!')
    else:
        print('Checking min deltas not work ok!')

    if check_cycle_builder():
        print('Cycle builder works ok')
    else:
        print('Cycle builder doesnt work ok')

if __name__ == '__main__':
    run_tests()