from dataclasses import dataclass, field

import aio_pika
from aio_pika.abc import AbstractRobustConnection

import orjson


@dataclass(slots=True)
class Emitter:
    rabbitmq_url: str
    connection: AbstractRobustConnection = field(init=False)

    async def run(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)

    async def emit(self, event_name: str, payload: dict) -> None:
        channel = await self.connection.channel()

        body = orjson.dumps(payload, default=str)
        await channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=event_name,
        )
