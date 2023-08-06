import asyncio
import sys
from decimal import Decimal
from architect_py.client import Client, Dir


async def main():
    client = Client()
    await client.connect()
    tradable_product = await client.get_tradable_product(
        base="BTC",
        quote="USD",
        venue="COINBASE")
    order_id = await client.send_limit_order(
        tradable_product_id=tradable_product["id"],
        dir=Dir.Buy,
        price="10000",
        quantity=Decimal("0.0005")
    )
    await asyncio.sleep(5)
    await client.cancel_order(order_id)
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
