import logging
import os
from typing import Any, Dict, Optional

from mpd import MPDClient


def connect() -> MPDClient:
    """Connect to Music Player Daemon

    Raises socker.error on connection failure.
    Raises mpd.CommandError on incorrect password.
    """

    logger = logging.getLogger("mpdbg")

    host: str = "localhost"
    port: int = 6600
    password: Optional[str] = None

    host_env = os.getenv("MPD_HOST", None)
    if host_env is not None:
        host_env_split = host_env.split("@", maxsplit=1)
        if len(host_env_split) == 2:
            password, host = host_env_split
        else:
            host = host_env

    port_env = os.getenv("MPD_PORT", None)
    if port_env is not None:
        try:
            port = int(port_env)
        except ValueError:
            logger.warning("invalid value in MPD_PORT environment variable (ignoring)")

    client = MPDClient()
    client.connect(host, port)

    if password is not None:
        client.password(password)

    return client


def read_picture(client: MPDClient, song: Dict[str, Any]) -> Optional[bytes]:
    # don't try to do readpicture for streams
    if song["file"].lower().startswith("http://") or song["file"].lower().startswith("https://"):
        return None

    image_data = client.readpicture(song["file"])
    if (image_data is None) or ("binary" not in image_data.keys()):
        return None

    return image_data["binary"]
