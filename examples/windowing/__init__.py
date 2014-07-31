from sobek import (
    gles2,
    error
)

import os

SOBEK_WINDOW_DEFAULT = "SDL"


def create_window(*args, **kwargs):
    window = SOBEK_WINDOW_DEFAULT

    if "SOBEK_WINDOW" in os.environ:
        window = os.environ["SOBEK_WINDOW"]

    window = window.lower()

    if window == "sfml":
        from . import sfml

        return sfml.SFMLWindow(*args, **kwargs)

    elif window == "sdl":
        from . import sdl

        return sdl.SDLWindow(*args, **kwargs)

    elif window == "pyglet":
        from . import pyglet

        return pyglet.PygletWindow(*args, **kwargs)

    elif window == "gtk":
        from . import gtk

        return gtk.GtkWindow(*args, **kwargs)

    else:
        raise RuntimeError(
            "SOBEK_WINDOW env variable incorrect; " +
            "must be one of: SFML, SDL, Pyglet or GTK."
        )


class Window:
    def _init(self, **kwargs):
        for key, val in kwargs.items():
            attr = key.lower()

            if hasattr(self, attr):
                setattr(self, attr, val)

        if not gles2.glew_init():
            raise error.Error("Couldn't initialize GLEW.")

    def main_loop(self, root, traversal, num_frames):
        pass
