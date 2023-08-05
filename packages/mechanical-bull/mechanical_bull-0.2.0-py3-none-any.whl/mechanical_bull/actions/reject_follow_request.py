import logging

from bovine import BovineClient

logger = logging.getLogger(__name__)


async def handle(client: BovineClient, data: dict):
    """Automatically rejects follow requests. Include via

    .. code-block:: toml

        [username.handlers]
        "mechanical_bull.actions.reject_follow_request" = true
    """
    if data["type"] != "Follow":
        return

    follow_actor = data["actor"]
    if isinstance(follow_actor, dict):
        follow_actor = follow_actor["id"]

    logger.info("Rejecting follow request from %s", follow_actor)

    reject = client.activity_factory.accept(data["id"], to={data["actor"]}).build()
    reject["type"] = "Reject"

    await client.send_to_outbox(reject)
