import atexit
import logging
import signal
import socket
import sys
import tempfile
import time
from typing import List, Optional, Union

import click
import mpd

from .image import create_wallpaper_image
from . import mpd_utils
from .wallpaper import WallpaperSetter


@click.group()
def cli():
    pass


@cli.command(help="run")
@click.option(
    "-w",
    "--wallpaper",
    "wallpaper",
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="The image file to use as wallpaper",
)
@click.option(
    "-s",
    "--wallpaper-setter",
    "wallpaper_setter",
    required=True,
    type=str,
    help="The wallpaper setter command. Use $image in command to insert quoted path to the image file.",
)
@click.option(
    "-e",
    "--effect",
    "effects",
    default=[],
    type=click.Choice(["blur", "grayscale"]),
    multiple=True,
    help="Effect to apply to wallpaper when displaying an album cover (multiple can be specified)",
)
@click.option(
    "-l",
    "--log-level",
    "log_level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error", "critical"]),
    help="Set log level.",
)
def run(wallpaper: str, wallpaper_setter: str, effects: List[str], log_level: str):
    logger = setup_logging(log_level)

    setter = WallpaperSetter(wallpaper_setter)

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    def reset_wallpaper():
        setter.try_set_wallpaper(wallpaper)

    def set_wallpaper(cover_data: Optional[bytes]):
        if cover_data is None:
            reset_wallpaper()
            return

        blur = "blur" in effects
        grayscale = "grayscale" in effects
        try:
            image = create_wallpaper_image(wallpaper, cover_data, blur, grayscale)
        except Exception as e:
            logger.error("failed to create wallpaper image: %s", e)
            reset_wallpaper()
            return

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            try:
                image_file.write(image)
            except Exception as e:
                reset_wallpaper()
                logger.error("failed to write temporary wallpaper file: %s", e)
                return
            setter.try_set_wallpaper(image_file.name)

    atexit.register(reset_wallpaper)

    reset_wallpaper()

    while True:
        try:
            client = mpd_utils.connect()
        except socket.error as e:
            logger.error("failed to connect to MPD: %s", e)
            time.sleep(5)
            continue
        except mpd.CommandError as e:
            logger.error("failed to connect to MPD (password error?): %s", e)
            time.sleep(5)
            continue

        logger.info("connected to MPD")

        try:
            song = {}
            state: str = "stop"

            while True:
                old_song = song
                song = client.currentsong()

                old_state = state
                state = client.status()["state"]

                if old_state == "play":
                    # change from play ...
                    if state == "play":
                        # ... to play
                        if song != old_song:
                            cover_data = mpd_utils.read_picture(client, song)
                            set_wallpaper(cover_data)
                    else:
                        # ... to stop or pause
                        reset_wallpaper()
                        pass
                else:
                    # change from stop or pause ...
                    if state == "play":
                        # ... to play
                        cover_data = mpd_utils.read_picture(client, song)
                        set_wallpaper(cover_data)
                    else:
                        # ... to stop or pause
                        # do nothing
                        pass

                client.idle()

        except Exception as e:
            logger.error("error in main loop: %s", e)
            reset_wallpaper()
            try:
                client.disconnect()
            except Exception:
                # ignore
                pass


def on_signal(sig, frame):
    if sig not in [signal.SIGINT, signal.SIGTERM]:
        return

    sys.exit(0)


def main():
    cli()


def setup_logging(level: Union[int, str]) -> logging.Logger:
    if isinstance(level, str):
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        level = level_map[level]

    logger = logging.getLogger("mpdbg")
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    return logger
