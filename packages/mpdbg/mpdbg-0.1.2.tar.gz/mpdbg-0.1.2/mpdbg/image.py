import io
import logging
import time

from PIL import Image, ImageOps, ImageFilter


def create_wallpaper_image(
        wallpaper_path: str, cover_data: bytes, blur: bool = False, grayscale: bool = False, image_format: str = "jpeg",
        cover_border_size: int = 10, cover_relative_size: float = 0.75, wallpaper_blur_radius: int = 20
) -> bytes:
    logger = logging.getLogger("mpdbg")

    start_time = time.perf_counter_ns()

    with open(wallpaper_path, "rb") as f:
        wallpaper = Image.open(f).convert("RGB")

    cover = Image.open(io.BytesIO(cover_data)).convert("RGB")

    # resize cover
    cover_scale = min(
        wallpaper.width / cover.width * cover_relative_size,
        wallpaper.height / cover.height * cover_relative_size,
    )
    cover = cover.resize(
        (int(cover.width * cover_scale), int(cover.height * cover_scale))
    )

    # add border to cover
    cover = ImageOps.expand(cover, cover_border_size, 0)

    if grayscale:
        # convert wallpaper to grayscale
        wallpaper = ImageOps.grayscale(wallpaper).convert("RGB")

    if blur:
        # blur wallpaper
        wallpaper = wallpaper.filter(ImageFilter.GaussianBlur(radius=wallpaper_blur_radius))

    # draw cover on wallpaper
    x = (wallpaper.width - cover.width) // 2
    y = (wallpaper.height - cover.height) // 2
    wallpaper.paste(cover, (x, y))

    # get image data
    wallpaper_bytes = io.BytesIO()
    wallpaper.save(wallpaper_bytes, image_format)
    wallpaper_data = wallpaper_bytes.getvalue()

    time_taken = time.perf_counter_ns() - start_time
    logger.debug("creating wallpaper image took %.3f seconds", time_taken / 1000 / 1000 / 1000)

    return wallpaper_data
