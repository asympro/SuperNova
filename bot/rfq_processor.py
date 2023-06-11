from collections import defaultdict

import chatgpt.chatgpt as chatgpt
import pricing.binance_connector as bc

last_rfq_by_user = defaultdict(lambda x: None)


def get_last_rfq(user):
    return last_rfq_by_user[user]


def process_request(request, user):
    parsed_request = chatgpt.parse_request(request)

    base_currency = parsed_request['base_currency']
    side = parsed_request['side']
    size = float(parsed_request.get('base_size'))
    notional_value = parsed_request.get('notional_value')

    if size:
        if side == 'both':
            buy_price, _ = bc.get_spot_price(base_currency, 'Buy', size)
            sell_price, _ = bc.get_spot_price(base_currency, 'Sell', size)
            message = f"The amount of money required to buy {size} {base_currency} on Binance's spot market is {buy_price} and to sell is {sell_price}"
        else:
            price, _ = bc.get_spot_price(base_currency, side, size)
            message = f"The amount of money required to {side} {size} {base_currency} on Binance's spot market is {price}"
    elif notional_value:
        spot_size, _ = bc.get_spot_size(base_currency, side, notional_value)
        message = f"The maximum size of {base_currency} that could be bought/sold on Binance's spot market with {notional_value} is {spot_size}."
    else:
        message = "Neither size nor notional_value is provided."

    last_rfq_by_user[user] = message
    return message
