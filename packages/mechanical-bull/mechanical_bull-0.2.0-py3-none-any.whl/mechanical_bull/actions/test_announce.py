from unittest.mock import AsyncMock, MagicMock

from .announce import handle


async def test_announces_activity_with_no_options():
    data = {"type": "Note"}

    client = AsyncMock()
    client.activity_factory = MagicMock()

    await handle(client, data)

    client.send_to_outbox.assert_awaited_once()


async def test_announces_activity_is_ignored():
    data = {"type": "Block"}

    client = AsyncMock()
    client.activity_factory = MagicMock()

    await handle(client, data, ignored_activities=["Block"])

    client.send_to_outbox.assert_not_awaited()


async def test_announces_activity_is_whitelisted():
    data = {"type": "Block"}

    client = AsyncMock()
    client.activity_factory = MagicMock()

    await handle(client, data, only_announce=["Create"])
    client.send_to_outbox.assert_not_awaited()

    data = {"type": "Create"}
    await handle(client, data, only_announce=["Create"])
    client.send_to_outbox.assert_awaited_once()


async def test_announces_activity_is_unwrapped():
    data = {"type": "Create", "object": "test"}

    client = AsyncMock()
    client.activity_factory = MagicMock()

    await handle(client, data, activties_to_announce_object=["Create"])
    client.send_to_outbox.assert_awaited_once()

    client.activity_factory.announce.assert_called_once()

    assert client.activity_factory.announce.call_args[0] == ("test",)
