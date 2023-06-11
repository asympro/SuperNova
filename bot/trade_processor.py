import chatgpt.chatgpt as chatgpt
import positions


def make_buy(message):
    result = ''
    base_curr = message['buy']['base_currency']
    base_size = message['buy']['base_size']
    current_pos = positions.get_position(base_curr)
    current_pos += base_size
    positions.set_position(base_curr, current_pos)

    result += f'SuperNova buys {base_size:.2f} of {base_curr}'
    if 'quote_size' in message['buy'] and message['buy']['quote_size']:
        quote_curr = message['buy']['quote_currency']
        quote_size = message['buy']['quote_size']
        current_pos = positions.get_position(quote_curr)
        current_pos -= quote_size
        positions.set_position(quote_curr, current_pos)

        result += f' and sells {quote_size:.2f} of {quote_curr}'

    return result


def make_sell(message):
    result = ''
    base_curr = message['sell']['base_currency']
    base_size = message['sell']['base_size']
    current_pos = positions.get_position(base_curr)
    current_pos -= base_size
    positions.set_position(base_curr, current_pos)

    result += f'SuperNova sells {base_size} of {base_curr}'
    if 'quote_size' in message['sell'] and message['sell']['quote_size']:
        quote_curr = message['sell']['quote_currency']
        quote_size = message['sell']['quote_size']
        current_pos = positions.get_position(quote_curr)
        current_pos += quote_size
        positions.set_position(quote_curr, current_pos)

        result += f' for {quote_size} of {quote_curr}'

    return result


def process_request(request, message):
    request = ''.join(request)
    if request == 'mine':
        if 'sell' in message:
            message = make_sell(message)
        else:
            return 'Error: you didn''t requested buy price'
    else:
        if 'buy' in message:
            message = make_buy(message)
        else:
            return 'Error: you didn''t requested sell price'
    return message


if __name__ == '__main__':
    msg = process_request('yours', {"buy": {
        "base_currency": "BTC",
        "base_size": 100,
        "quote_currency": 'ETH',
        "quote_size": 25}})
    print(msg)
    pos = positions.get_position('BTC')
    print(pos)
    pos = positions.get_position('ETH')
    print(pos)

    msg = process_request('mine', {"sell": {
        "base_currency": "BTC",
        "base_size": 100,
        "quote_currency": 'ETH',
        "quote_size": 25}})
    print(msg)
    pos = positions.get_position('BTC')
    print(pos)
    current_pos = positions.get_position('ETH')
    print(pos)
