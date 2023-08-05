import logging

from typing import List
from bovine import BovineClient

logger = logging.getLogger(__name__)


async def handle(
    client: BovineClient,
    data: dict,
    activties_to_announce_object: List[str] = [],
    only_announce: List[str] | None = None,
    ignored_activities: List[str] = [],
):
    """Automatically announces objects. Announces are public.
    In order to allow for non public announces, one probably needs
    `FEP-8b32 <https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-8b32.md>`_
    as discussed `here <https://socialhub.activitypub.rocks/t/use-cases-of-fep-8b32-object-integrity-proofs/3249/5?u=helge>`_.

    .. code-block:: toml

        [username.handlers."mechanical_bull.actions.announce"]
        activties_to_announce_object = ["Create"]
        only_announce = ["Create"]

        [username.handlers."mechanical_bull.actions.announce"]
        ignored_activities = ["Block"]

    The first configuration will cause the handler to announce an object of a create.
    This behavior is similar to the behavior of boosting every toot on Mastodon.
    The second configuration is similar to what Lemmy does.

    To use as a handler in python code use

    .. code-block:: python

        from functools import partial

        values = {"ignored_activities": ["Block"]}
        return partial(handle, **value)
    """
    if "type" not in data:
        return

    if data["type"] in ignored_activities:
        return

    if only_announce:
        if data["type"] not in only_announce:
            return

    if data["type"] in activties_to_announce_object:
        if "object" not in data:
            return
        data = data["object"]

    activity = client.activity_factory.announce(data).as_public().build()

    await client.send_to_outbox(activity)
