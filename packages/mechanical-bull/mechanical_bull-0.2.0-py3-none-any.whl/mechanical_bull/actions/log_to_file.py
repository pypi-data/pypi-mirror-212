import json

from bovine import BovineClient


async def handle(actor: BovineClient, data: dict, filename=None) -> None:
    """Logs all activity to the file given by filename. To use
    in your configuration file use

    .. code-block:: toml

        [username.handlers."mechanical_bull.actions.log_to_file"]
        filename = "logfile.txt"

    To use as a handler in python code use

    .. code-block:: python

        from functools import partial

        values = {"filename": "logfile.txt"}
        return partial(func, **value)

    """
    if filename:
        with open(filename, "a") as fp:
            fp.write(json.dumps(data, indent=2))
            fp.write("\n")
