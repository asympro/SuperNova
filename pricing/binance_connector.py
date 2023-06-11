import requests


def __init__():
    pass


def get_hedge_size(base_currency, side, requested_price):
    r = requests.get(f'https://fapi.binance.com/fapi/v1/depth?symbol={base_currency}USDT&limit=1000')
    if r.status_code == 200:
        j = r.json()
        book = j['bids'] if side == 'Sell' or side == 'bid' else j['asks']

        total_size = 0
        remain_money = float(requested_price)
        for price, size in book:
            size = float(size)
            price = float(price)
            level_price = price * size
            if level_price < remain_money:
                total_size += size
                remain_money -= level_price
            else:
                total_size += remain_money / price
                remain_money = 0
                break

        return total_size, remain_money
    elif r.status_code == 404:
        return None


def get_spot_size(base_currency, side, requested_price):
    r = requests.get(f'https://api.binance.com/api/v3/depth?symbol={base_currency}USDT&limit=5000')
    if r.status_code == 200:
        j = r.json()
        book = j['bids'] if side == 'Sell' or side == 'bid' else j['asks']

        total_size = 0
        remain_money = float(requested_price)
        for price, size in book:
            size = float(size)
            price = float(price)
            level_price = price * size
            if level_price < remain_money:
                total_size += size
                remain_money -= level_price
            else:
                total_size += remain_money / price
                remain_money = 0
                break

        return total_size, remain_money
    elif r.status_code == 404:
        return None


def get_hedge_price(base_currency, side, requested_size):
    r = requests.get(f'https://fapi.binance.com/fapi/v1/depth?symbol={base_currency}USDT&limit=1000')
    if r.status_code == 200:
        j = r.json()
        book = j['bids'] if side == 'Sell' or side == 'bid' else j['asks']

        total_spend = 0
        remain_size = float(requested_size)
        for price, size in book:
            size = float(size)
            price = float(price)
            if size < remain_size:
                total_spend += price * size
                remain_size -= size
            else:
                total_spend += price * remain_size
                remain_size = 0
                break

        return total_spend, remain_size
    elif r.status_code == 404:
        return None


def get_spot_price(base_currency, side, requested_size):
    r = requests.get(f'https://api.binance.com/api/v3/depth?symbol={base_currency}USDT&limit=5000')
    if r.status_code == 200:
        j = r.json()
        book = j['bids'] if side == 'Sell' or side == 'bid' else j['asks']

        total_spend = 0
        remain_size = float(requested_size)
        for price, size in book:
            size = float(size)
            price = float(price)
            if size < remain_size:
                total_spend += price * size
                remain_size -= size
            else:
                total_spend += price * remain_size
                remain_size = 0
                break

        return total_spend, remain_size

    elif r.status_code == 404:
        return None


if __name__ == '__main__':
    print(get_spot_price('BTC', 'Sell', 150))
    print(get_spot_price('BTC', 'Buy', 150))
    print(get_hedge_price('BTC', 'Sell', 150))
    print(get_hedge_price('BTC', 'Buy', 150))

    print(get_spot_size('BTC', 'Sell', 1000000))
    print(get_spot_size('BTC', 'Sell', 10000000))
    print(get_spot_size('BTC', 'Buy', 1000000))
    print(get_spot_size('BTC', 'Buy', 10000000))

    print(get_hedge_size('BTC', 'Sell', 1000000))
    print(get_hedge_size('BTC', 'Buy', 1000000))
