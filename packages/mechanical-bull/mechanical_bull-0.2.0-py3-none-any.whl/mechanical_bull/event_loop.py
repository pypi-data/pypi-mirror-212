import asyncio

import bovine
import json

import logging

logger = logging.getLogger(__name__)


async def handle_connection(client: bovine.BovineClient, handlers: list):
    """Opens an event source and applies all handlers to captured events.

    :param handlers:

        list of methods taking at argument the BovineClient client and
        a dictionary representing the ActivityPub activity."""
    event_source = await client.event_source()
    logger.info("Connected")
    async for event in event_source:
        if not event:
            return
        if event and event.data:
            data = json.loads(event.data)
            logger.debug(event.data)

            for handler in handlers:
                await handler(client, data)


async def handle_connection_with_reconnect(
    client: bovine.BovineClient,
    handlers: list,
    client_name: str = "BovineClient",
    wait_time: int = 10,
):
    """As handle_connection, but automatically recoonects after wait_time many seconds.

    :param client_name:

        Used for logging purpose

    :param wait_time:

        Time in seconds to wait between connection attempts."""
    while True:
        await handle_connection(client, handlers)
        logger.info(
            "Disconnected from server for %s, reconnecting in %d seconds",
            client_name,
            wait_time,
        )
        await asyncio.sleep(wait_time)


async def loop(client_name, client_config, handlers):
    while True:
        try:
            async with bovine.BovineClient(client_config) as client:
                await handle_connection_with_reconnect(
                    client, handlers, client_name=client_name
                )
        except Exception as e:
            logger.exception("Something went wrong for %s", client_name)
            logger.exception(e)
            await asyncio.sleep(60)
