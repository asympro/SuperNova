import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

instructions = 'I am working at a crypto trading company and responsible for the OTC desk. Our counterparties send ' \
               '"request for quote" requests in plain text. Please help me parse the requests. The request has at ' \
               'least two currencies: base currency - this is the currency counterparty wants to buy or sell. Quote ' \
               'currency - the currency which will be used to buy or sell. If the request is only a number and ' \
               'currency like "100 BTC" this means that the base is BTC, the Base size 100, and the quote currency by ' \
               'default is USD. If the size in dollars like 100$ BTC. This means Base is BTC, Base size is empty, ' \
               'USD is quote currency. Also there is a notion value sometimes, this means that size mentioned in USD ' \
               'value, like "1,000,000$ BTC to ETH" - means that BTC is base, ETH is quote, base size is empty, ' \
               'quote size is empty notion value is 1,000,000.  2w or 2 ways means that both bid and ask are ' \
               'requested. The price could be requested against twap or vwap, this will be additional info. I ' \
               'will send you the request, and you need to return only the following information as JSON. ' \
               'Request "Can I have an offer in 10 BTC", means that side is ask' \
               'Request "Id like to buy 20 BTC", means that side is ask' \
               'If counterparty request is that it is want to buy something, means that side is ask' \
               'If counterparty request is that it is want to sell something, means that side is bid' \
               'If BTCE, BITO, BITS is base currency, quote currency is always USD' \
               'Return only json. Fields in json: "side", "base_currency", "base_size", "quote_currency", ' \
               '"quote_size", "notional_value", "settlement", "is_nav", "additional_info". Side (' \
               'bid/ask/both)? What is the base? What is the size in the base currency? What is the notion value? ' \
               'What is the quote currency? If it is a symbol, change it to the currency''s short name.\
                What is the size in the quote currency?\
                What is the settlement day?\
                Is it an NAV request?\
                Additional info' \
               'Return only json.'


def extract_json(s):
    start = s.find('{')
    end = s.find('}', start)
    return s[start:end+1]


def parse_request(req):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": req}
        ]
    )
    # completion = openai.Completion.create(
    #     model="davinci:ft-personal:super-nova-rfq-2023-06-11-10-49-04",
    #     prompt=instructions,
    #     max_tokens=1000,
    #     temperature=0
    # )

    try:
        content = completion.choices[0].message['content']
        extract = extract_json(content)
        return json.loads(extract)
    except json.decoder.JSONDecodeError:
        return None


if __name__ == '__main__':
    text = ['2w 500 BTC',
            'Can I have an offer in 10 BTC',
            'Id like to buy 20 BTC',
            'NAV 2w BTCE GY todays NAV settlement t+2',
            'Can i have a 2way in 10,000,000$ BTC',
            'What can you show 2w 10000 BTC against 1d twap/vwap',
            'I would like to swap 1,000,000 $ BTC to ETH']

    for line in text:
        parsed = parse_request(line)
        print(parsed, line)
