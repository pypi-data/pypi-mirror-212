import logging
import shlex
import time
from string import Template
import subprocess


class WallpaperSetter:
    def __init__(self, command: str):
        self.logger = logging.getLogger("mpdbg")
        self.command_template = Template(command)

    def set_wallpaper(self, wallpaper_path: str):
        """Set the desktop wallpaper.

        Raises CalledProcessError if executing wallpaper setter returns non-zero."""

        start_time = time.perf_counter_ns()
        command_line = self.command_template.safe_substitute(image=shlex.quote(wallpaper_path))
        subprocess.run(command_line, check=True, capture_output=True, shell=True)
        time_taken = time.perf_counter_ns() - start_time
        self.logger.debug("setting wallpaper took %.3f seconds", time_taken / 1000 / 1000 / 1000)

    def try_set_wallpaper(self, wallpaper_path: str):
        try:
            self.set_wallpaper(wallpaper_path)
        except subprocess.CalledProcessError as e:
            self.logger.error("failed to set wallpaper: %s", e.output.decode())
