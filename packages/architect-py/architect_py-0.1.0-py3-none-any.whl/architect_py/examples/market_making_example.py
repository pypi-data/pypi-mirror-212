import asyncio
from decimal import Decimal
from architect_py.client import Client, Dir


async def main():
    client = Client()
    await client.connect()
    tradable_product = await client.get_tradable_product(
        base="BTC",
        quote="USD",
        venue="COINBASE")
    quote_increment = Decimal(
        tradable_product["trade_info"]["quote_increment"])

    def round_price(price):
        return Decimal(round(price / quote_increment) * quote_increment)

    book_updates = await client.subscribe({
        "type": "SubscribeBook",
        "tradable_product": tradable_product["id"],
        "width": 1
    })
    min_away, target_away, max_away = (
        Decimal(0.9978), Decimal(0.998), Decimal(0.9982))
    last_sent = None

    while True:
        book_update = await book_updates.get()
        best_bid = Decimal(book_update["buy"][0]["price"])
        if best_bid <= 0:
            continue
        if last_sent:
            last_sent_price, last_sent_oid = last_sent
            away = last_sent_price / best_bid
            if away > max_away or away < min_away:
                await client.cancel_order(last_sent_oid)
                last_sent = None
        else:
            target_price = round_price(best_bid * target_away)
            order_id = await client.send_limit_order(
                tradable_product_id=tradable_product["id"],
                dir=Dir.Buy,
                price=target_price,
                quantity=Decimal("0.0002")
            )
            last_sent = (target_price, order_id)

if __name__ == "__main__":
    asyncio.run(main())
