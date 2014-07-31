import pyglet
import time

from . import window

pyglet.options["debug_gl"] = False


class PygletWindow(window.Window):
    def __init__(self, width, height, **kwargs):
        window.Window.__init__(self, width, height)

        self.window = pyglet.window.Window(width=width, height=height)

        self._frames = 0

        self._init(**kwargs)

    def main_loop(self, root, traversal):
        start = time.time()

        @self.window.event
        def on_draw(*args):
            root.traverse(traversal)

            self._frames += 1

        @self.window.event
        def on_close(*args):
            self.window.close()

        pyglet.clock.schedule_interval(lambda dt: None, 1.0 / 60.0)
        # NOTE: This function call is, supposedly, no longer needed.
        # pyglet.clock.set_fps_limit(60.0)

        ipython_found = False

        try:
            __IPYTHON__

            ipython_found = True

        except NameError:
            pass

        if ipython_found:
            from IPython.lib.inputhook import enable_pyglet

            enable_pyglet()

        else:
            pyglet.app.run()

        return self._frames / (time.time() - start)

    def set_fullscreen(self, fullscreen):
        self.fullscreen = fullscreen

        self.window.set_fullscreen(fullscreen)

    def set_vsync(self, vsync):
        self.vsync = vsync

        self.window.set_vsync(vsync)

    def set_title(self, title):
        self.title = title

        self.window.set_caption(title)
