import asyncio
from architect_py.client import Client


async def main():
    client = Client()
    await client.connect()
    updates = await client.subscribe_netidx('/local/architect/core/clock')
    while True:
        print(await updates.get())


if __name__ == "__main__":
    asyncio.run(main())
