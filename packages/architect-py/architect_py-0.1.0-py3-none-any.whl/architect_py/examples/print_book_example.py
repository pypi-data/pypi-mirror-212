import asyncio
import os
from architect_py.client import Client

buy_columns = '{:>15} {:>15} {:>15}'
sell_columns = '{:<15} {:<15} {:<15}'
green = '\033[32m'
red = '\033[31m'
normal = '\033[0m'


def print_book(book):
    os.system('clear')  # Clear the terminal
    print((buy_columns + ' ' + sell_columns).format(
        "Total", "Size", "Bid", "Ask", "Size", "Total"))
    for i in range(min(20, len(book['buy']), len(book['sell']))):
        b = book['buy'][i]
        s = book['sell'][i]
        print(
            (green + buy_columns).format(b['total'], b['size'], b['price']),
            (red + sell_columns).format(s['price'], s['size'], s['total'])
        )
    print(normal)


async def main():
    client = Client()
    await client.connect()
    tradable_product = await client.get_tradable_product(
        base="BTC",
        quote="USD",
        venue="COINBASE")
    book_updates = await client.subscribe({
        "type": "SubscribeBook",
        "tradable_product": tradable_product["id"],
        "width": 1
    })
    while True:
        book_update = await book_updates.get()
        print_book(book_update)

if __name__ == "__main__":
    asyncio.run(main())
