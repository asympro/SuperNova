from collections import defaultdict

positions_by_symbol = defaultdict(float)


def get_position(symbol):
    return positions_by_symbol[symbol]


def set_position(symbol, position):
    positions_by_symbol[symbol] = position
