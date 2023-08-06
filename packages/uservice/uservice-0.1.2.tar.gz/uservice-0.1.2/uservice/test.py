import asyncio
import json
from aio_pika import connect, Message

from .main import Test


async def main():
    connection = await connect()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.get_exchange('test')
        print("ello")
        for i in range(1):
            await exchange.publish(
                Message(body=json.dumps(Test(foo=i).dict()).encode()),
                routing_key='event'
            )



if __name__ == '__main__':
    asyncio.run(main())
