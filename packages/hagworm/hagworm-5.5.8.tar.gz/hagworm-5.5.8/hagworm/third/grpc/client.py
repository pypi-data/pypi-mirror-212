# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import queue
import asyncio
import grpc
import msgpack


CHANNEL_USABLE_STATE = (grpc.ChannelConnectivity.READY, grpc.ChannelConnectivity.IDLE)
CHANNEL_READY_TIMEOUT = 1


class GRPCClient:

    __slots__ = [
        r'_channel_queue', r'_credentials', r'_options', r'_compression', r'_interceptors',
        r'_request_serializer', r'_response_deserializer',
    ]

    def __init__(
        self, *,
        credentials=None, options=None, compression=None, interceptors=None,
        request_serializer=msgpack.dumps, response_deserializer=msgpack.loads
    ):

        self._channel_queue: queue.SimpleQueue[grpc.aio.Channel] = queue.SimpleQueue()

        self._credentials = credentials
        self._options = options
        self._compression = compression
        self._interceptors = interceptors

        self._request_serializer = request_serializer
        self._response_deserializer = response_deserializer

    async def _make_channel(self, target) -> grpc.aio.Channel:

        channel = None

        try:

            if self._credentials is None:
                channel = grpc.aio.insecure_channel(
                    target, self._options, self._compression, self._interceptors
                )
            else:
                channel = grpc.aio.secure_channel(
                    target, self._credentials, self._options, self._compression, self._interceptors
                )

            await asyncio.wait_for(channel.channel_ready(), CHANNEL_READY_TIMEOUT)

        except asyncio.TimeoutError as err:

            await channel.close()

            raise err

        setattr(channel, r'name', target)

        return channel

    async def open(self, targets):

        await self.set_channel(targets)

    async def close(self):

        while not self._channel_queue.empty():
            channel = self._channel_queue.get_nowait()
            await channel.close()

    async def get_channel(self) -> grpc.aio.Channel:

        channel = None

        for _ in range(self._channel_queue.qsize()):

            self._channel_queue.put_nowait(
                channel := self._channel_queue.get_nowait()
            )

            if channel.get_state() in CHANNEL_USABLE_STATE:
                break

        return channel

    async def set_channel(self, targets):

        channel_dict = {}

        while not self._channel_queue.empty():
            channel = self._channel_queue.get_nowait()
            channel_dict[getattr(channel, r'name')] = channel

        for target in targets:
            if target not in channel_dict:
                channel_dict[target] = await self._make_channel(target)

        for target, channel in channel_dict.items():
            if target in targets:
                self._channel_queue.put_nowait(channel)
            else:
                await channel.close()

    async def unary_unary(self, method: str, call_params: typing.Dict):

        channel = await self.get_channel()

        return await channel.unary_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def unary_stream(self, method: str, call_params: typing.Dict):

        channel = await self.get_channel()

        return await channel.unary_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def stream_unary(self, method: str, call_params: typing.Dict):

        channel = await self.get_channel()

        return await channel.stream_unary(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)

    async def stream_stream(self, method: str, call_params: typing.Dict):

        channel = await self.get_channel()

        return await channel.stream_stream(
            method,
            request_serializer=self._request_serializer,
            response_deserializer=self._response_deserializer,
        )(call_params)
