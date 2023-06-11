from collections import defaultdict

import chatgpt.chatgpt as chatgpt
import pricing.binance_connector as bc

last_rfq_by_user = defaultdict(lambda x: None)


def get_last_rfq(user):
    return last_rfq_by_user[user]


def process_request(request, user):
    parsed_request = chatgpt.parse_request(request)

    base_currency = parsed_request['base_currency']
    quote_currency = parsed_request['quote_currency']
    quote_size = parsed_request['quote_size']
    side = parsed_request['side']

    size = None
    if 'base_size' in parsed_request and parsed_request['base_size']:
        size = float(parsed_request.get('base_size'))
    notional_value = parsed_request['notional_value']

    curr_rfq = {}

    if size:
        if side == 'both':
            buy_price, _ = bc.get_spot_price(base_currency, 'Buy', size)
            sell_price, _ = bc.get_spot_price(base_currency, 'Sell', size)

            curr_rfq["buy"] = {}
            curr_rfq["buy"]['base_currency'] = base_currency
            curr_rfq["buy"]['base_size'] = size
            curr_rfq["buy"]['quote_currency'] = quote_currency
            curr_rfq["buy"]['quote_size'] = sell_price

            curr_rfq["sell"] = {}
            curr_rfq["sell"]['base_currency'] = base_currency
            curr_rfq["sell"]['base_size'] = size
            curr_rfq["sell"]['quote_currency'] = quote_currency
            curr_rfq["sell"]['quote_size'] = buy_price

            message = f"SuperNova sells {size:.2f} {base_currency} for {sell_price:.2f} and buys for {buy_price:.2f}"
        else:
            price, _ = bc.get_spot_price(base_currency, side, size)
            if side == 'bid':
                side = 'buys'
            else:
                side = 'sells'
            message = f"SuperNova {side} {size} {base_currency} for {price:.2f}"
    elif notional_value:
        if isinstance(notional_value,str):
            notional_value = notional_value.replace(',', '')
            notional_value = notional_value.replace("'", '')

        notional_value = float(notional_value)

        buy_price, _ = bc.get_spot_price(base_currency, 'Buy', notional_value)
        sell_price, _ = bc.get_spot_price(base_currency, 'Sell', notional_value)

        quote_price = bc.get_mid_price(quote_currency)
        bace_price = bc.get_mid_price(base_currency)

        curr_rfq["buy"] = {}
        curr_rfq["buy"]['base_currency'] = base_currency
        curr_rfq["buy"]['base_size'] = notional_value / bace_price
        curr_rfq["buy"]['quote_currency'] = quote_currency
        curr_rfq["buy"]['quote_size'] = buy_price / quote_price

        curr_rfq["sell"] = {}
        curr_rfq["sell"]['base_currency'] = base_currency
        curr_rfq["sell"]['base_size'] = size
        curr_rfq["sell"]['quote_currency'] = quote_currency
        curr_rfq["sell"]['quote_size'] = sell_price / quote_price

        buy_size = curr_rfq["buy"]['base_size']
        buy_price = curr_rfq["buy"]['quote_size']
        sell_price = curr_rfq["sell"]['quote_size']
        message = f"SuperNova sells {buy_size} of {base_currency} for {sell_price:.2f} of {quote_currency} and buys for {buy_price:.2f} of {quote_currency}"

    else:
        message = "Neither size nor notional_value is provided."

    last_rfq_by_user[user] = curr_rfq
    return message


if __name__ == '__main__':
    msg = process_request('I would like to swap 1,000,000 $ BTC to ETH', 'evgen')
    print(msg)
