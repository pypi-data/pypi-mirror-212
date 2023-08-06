import asyncio
import json
import logging
import websockets
from decimal import Decimal
from enum import Enum
from sys import exit
from typing import Any, Dict


class Dir(Enum):
    Buy = 1
    Sell = 2


class ProductType(Enum):
    Crypto = 1
    Fiat = 2


class Client:
    def __init__(self, base_ws_url: str = 'ws://127.0.0.1:6001'):
        self.base_ws_url = base_ws_url
        self.id = 0
        self.pending_netidx_subcriptions = []
        self.netidx_subid_to_path = {}
        self.netidx_subscriptions = {}
        self.pending_rpcs = {}
        self.subscriptions = {}
        self.websocket_core = None
        self.websocket_netidx = None
        self.authenticated = asyncio.Future()

    async def connect(self):
        self.websocket_core = await websockets.connect(f'{self.base_ws_url}/architect', ping_interval=5)
        self.websocket_netidx = await websockets.connect(f'{self.base_ws_url}/netidx', ping_interval=5)
        asyncio.create_task(self.__task())
        await self.authenticated

    async def query(self, request: Dict[str, Any]) -> Any:
        id = self.__attach_id(request)
        self.pending_rpcs[id] = asyncio.Future()
        Log.debug(f'Sent query to Architect (core): {request}')
        await self.websocket_core.send(json.dumps(request))
        return await self.pending_rpcs[self.id]

    async def subscribe(self, request: Dict[str, Any]) -> asyncio.Queue:
        id = self.__attach_id(request)
        self.subscriptions[id] = asyncio.Queue()
        Log.debug(f'Sent subscription to Architect (core): {request}')
        await self.websocket_core.send(json.dumps(request))
        return self.subscriptions[id]

    async def subscribe_netidx(self, path: str) -> asyncio.Queue:
        subscriptions = self.netidx_subscriptions.get(path, [])
        is_new = len(subscriptions) == 0
        subscriptions.append(asyncio.Queue())
        self.netidx_subscriptions[path] = subscriptions
        if is_new:
            self.pending_netidx_subcriptions.append(path)
            request = {
                "type": "Subscribe",
                "path": path,
            }
            Log.debug(f'Sent subscription to Architect (netidx): {request}')
            await self.websocket_netidx.send(json.dumps(request))
        return subscriptions[-1]

    async def get_tradable_product(
            self,
            base: str,
            quote: str,
            venue: str,
            base_type: ProductType = ProductType.Crypto,
            quote_type: ProductType = ProductType.Fiat,
            route: str = 'DIRECT'
    ) -> Dict[str, Any]:
        pat = f'{base}{self.__product_type_suffix(base_type)}/{quote}{self.__product_type_suffix(quote_type)}*{venue}/{route}'
        tps = (await self.query({
            "type": "SearchSymbol",
            "limit": 1,
            "pat": pat,
            "scope": "TradableProduct"
        }))["tradable_product"]
        if len(tps) == 0:
            raise Exception(
                f'No tradable products found that match pattern: {pat}')
        id = tps[0][1]
        tps = await self.query({
            "type": "GetTradableProductDetails",
            "tradable_product": [id]
        })
        if len(tps) == 0:
            raise Exception(
                f'Could not fetch tradable product details for id: {id}')
        return tps[0]

    async def send_limit_order(self, tradable_product_id: str, dir: Dir, price: Decimal, quantity: Decimal, account: str = "Default") -> int:
        return await self.query({
            "type": "SendLimitOrder",
            "account": account,
            "dir": dir.name,
            "price": str(price),
            "quantity": str(quantity),
            "target": tradable_product_id
        })

    async def cancel_order(self, order_id: str) -> None:
        return await self.query({
            "type": "CancelOrder",
            "order_id": order_id
        })

    async def __websocket_netidx_handler(self):
        while True:
            message = json.loads(await self.websocket_netidx.recv())
            if typ := message.get('type'):
                if typ == 'Subscribed':
                    id = message['id']
                    assert (len(self.pending_netidx_subcriptions) > 0)
                    self.netidx_subid_to_path[id] = self.pending_netidx_subcriptions.pop(
                        0)
                elif typ == 'Update':
                    if updates := message.get("updates"):
                        for update in updates:
                            id = update['id']
                            path = self.netidx_subid_to_path[id]
                            event = update['event']
                            value = event['value']
                            for subscription in self.netidx_subscriptions[path]:
                                await subscription.put(value)

    def __process_hello_message(self, hello_message: str):
        if hello_message == 'Normal':
            Log.info(f'Architect authorized')
            self.authenticated.set_result(())
        elif hello_message == 'Trial':
            Log.info(f'Architect authorized (trial mode)')
            self.authenticated.set_result(())
        elif hello_message == 'FirstRun':
            Log.info('Architect not yet setup. Please run GUI first.')
            exit(1)
        elif hello_message == 'NotLicensed':
            Log.info('Architect not licensed. Please purchase license via GUI.')
            exit(1)
        else:
            Log.info(f'Unrecognized Hello message: {hello_message}')
            exit(1)

    async def __websocket_core_handler(self):
        hello_message = json.loads(await self.websocket_core.recv())
        self.__process_hello_message(hello_message)
        async for data in self.websocket_core:
            message = json.loads(data)
            if id := message.get('id'):
                if future := self.pending_rpcs.pop(id, None):
                    future.set_result(self.__extract_ok(message))
                elif queue := self.subscriptions.get(id, None):
                    await queue.put(self.__extract_ok(message))

    async def __task(self):
        await asyncio.gather(
            self.__websocket_core_handler(),
            self.__websocket_netidx_handler(),
        )

    def __attach_id(self, message: Dict[str, Any]) -> int:
        self.id += 1
        message['id'] = self.id
        return self.id

    def __extract_ok(self, response: Dict[str, Any]) -> Any:
        if "response" not in response:
            raise Exception(
                f'Expected "response" key in response: {response}')
        inner_response = response["response"]
        if "Ok" in inner_response:
            return inner_response["Ok"]
        if "Err" in inner_response:
            raise Exception(
                f'Encountered error in response: {inner_response["Err"]}')
        raise Exception(f'Expected "Ok" or "Err" in response: {response}')

    def __product_type_suffix(self, product_type: ProductType) -> str:
        if product_type == ProductType.Fiat:
            return ''
        return f' {product_type.name}'


def __log(name: str):
    log = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s|%(name)s|%(levelname)s|%(message)s')
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    log.setLevel(logging.DEBUG)
    return log


Log = __log('Architect')
