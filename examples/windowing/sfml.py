from . import window

import sfml
import time


class SFMLWindow(window.Window):
    DEFAULT_STYLE = sfml.window.Style.TITLEBAR | sfml.window.Style.CLOSE

    def __init__(self, width, height, **kwargs):
        window.Window.__init__(self, width, height)

        self.context = sfml.ContextSettings()

        self.context.depth_bits = 16
        self.context.stencil_bits = 8
        self.context.major_version = 2
        self.context.minor_version = 0

        self.window = sfml.window.Window(
            sfml.window.VideoMode(width, height),
            "SFMLWindow",
            SFMLWindow.DEFAULT_STYLE,
            self.context
        )

        self._init(**kwargs)

    def main_loop(self, root, traversal):
        frames = 0
        start = time.time()

        while self.window.is_open:
            for event in self.window.events:
                if event == sfml.window.CloseEvent:
                    self.window.close()

                elif (
                    event == sfml.window.KeyEvent and
                    event.code == sfml.window.Keyboard.ESCAPE
                ):
                    self.window.close()

            root.traverse(traversal)

            self.window.display()

            frames += 1

        return frames / (time.time() - start)

    def set_fullscreen(self, fullscreen):
        self.fullscreen = fullscreen

        self.window.recreate(
            sfml.window.VideoMode(*self.size),
            self.title,
            (
                fullscreen and
                sfml.window.Style.FULLSCREEN or
                SFMLWindow.DEFAULT_STYLE
            ),
            self.context
        )

    def set_vsync(self, vsync):
        self.vsync = vsync

        self.window.vertical_synchronization = vsync

    def set_title(self, title):
        self.title = title

        self.window.title = title
