import asyncio
import uuid
import aiormq
import aiormq.abc
from schemas.telegram import TelegramUpdate
from schemas.worker_request import WorkerRequest


class RpcClient:
    def __init__(self, loop):
        self.connection = None      # type: aiormq.Connection
        self.channel = None         # type: aiormq.Channel
        self.callback_queue = ''
        self.futures = {}
        self.loop = loop

    async def connect(self):
        # TODO: create config option
        self.connection = await aiormq.connect("amqp://guest:guest@localhost/")

        self.channel = await self.connection.channel()
        declare_ok = await self.channel.queue_declare(
            exclusive=True, auto_delete=True
        )

        await self.channel.basic_consume(declare_ok.queue, self.on_response)

        self.callback_queue = declare_ok.queue

        return self

    async def on_response(self, message: aiormq.abc.DeliveredMessage):
        future = self.futures.pop(message.header.properties.correlation_id)
        future.set_result(message.body)

    async def call(self, function_name: str, update: TelegramUpdate):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()

        request = WorkerRequest(function_name=function_name, update=update)

        self.futures[correlation_id] = future

        await self.channel.basic_publish(
            request.model_dump_json().encode(), routing_key='rpc_queue', # TODO: create config option
            properties=aiormq.spec.Basic.Properties(
                content_type='application/json',
                correlation_id=correlation_id,
                reply_to=self.callback_queue,
            )
        )

        return await future
