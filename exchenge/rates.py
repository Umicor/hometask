import asyncio
import aiohttp
from pprint import pprint as print

api_key = "IZRRWQVEBQROCMXL"


async def fetch_exchange_rate(session, from_currency, to_currency):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={api_key}'

    async with session.get(url) as response:
        data = await response.json()
        return data


async def main():
    source_currencies = ['uah', 'gbp']
    target_currency = 'usd'

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_exchange_rate(session, source_currency, target_currency) for source_currency in
                 source_currencies]
        results = await asyncio.gather(*tasks)

        for source_currency, result in zip(source_currencies, results):
            print(f'Обменный курс от {source_currency.upper()} к {target_currency.upper()}:')
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
