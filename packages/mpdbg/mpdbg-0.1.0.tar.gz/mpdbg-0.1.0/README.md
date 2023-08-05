# mpdbg

## About

*mpdbg* is a program that listens to a [Music Player Daemon](https://www.musicpd.org) and changes the desktop wallpaper image depending on the current song. If the song has a cover art image, it will be drawn on top of wallpaper. A couple of effects can be applied to original wallpaper in this case, if user chooses so. If the current song doesn't have a cover art image, the original wallpaper wil be displayed.

Check out [mpdbg's homepage](https://git.dragonwit.dev/dragonwit/mpdbg-py) for downloads and such.

## Installation

*mpdbg* is not in the [Python Package Index (PyPI)](https://pypi.org) and I have no plans currently to put it there. You can install the program by downloading *mpdbg-x.y.z-py3-none-any.whl* from project's releases page and running:

    pip install --user ./mpdbg-x.y.z-py3-none-any.whl

This would install *mpdbg* for current user and an excutable script to *~/.local/bin/mpdbg*.

## Building

Install [poetry](https://python-poetry.org) and execute following in the project directory:

    poetry build

## Usage

    Usage: mpdbg run [OPTIONS]
    
      run
    
    Options:
      -w, --wallpaper FILE            The image file to use as wallpaper
                                      [required]
      -s, --wallpaper-setter TEXT     The wallpaper setter command. Use $image in
                                      command to insert quoted path to the image
                                      file.  [required]
      -e, --effect [blur|grayscale]   Effect to apply to wallpaper when displaying
                                      an album cover (multiple can be specified)
      -l, --log-level [debug|info|warning|error|critical]
                                      Set log level.
      --help                          Show this message and exit.

Example for using *mpdbg* with [swww](https://github.com/Horus645/swww) wallpaper setter:

    mpdbg run -w ~/wallpaper.png -s 'swww img --transition-type center $image' -e blur

The command above would use *~/wallpaper.png* as wallpaper and *swww* as wallpaper setter. The wallpaper would also be blurred when displaying a cover art image on top of it.

