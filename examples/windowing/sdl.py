import ctypes
import sdl2
import time

from . import Window


class SDLWindow(Window):
    def __init__(self, width, height, **kwargs):
        Window.__init__(self)

        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

        self.window = sdl2.SDL_CreateWindow(
            b"SDLWindow",
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            width,
            height,
            sdl2.SDL_WINDOW_OPENGL
        )

        self.context = sdl2.SDL_GL_CreateContext(self.window)

        self._init(**kwargs)

    def main_loop(self, root, traversal, num_frames=0):
        frames = 0
        start = time.time()
        event = sdl2.SDL_Event()
        running = True

        def quit_condition(event):
            return any((
                event.type == sdl2.SDL_QUIT,
                (
                    event.type == sdl2.SDL_KEYUP and
                    event.key.keysym.sym == sdl2.SDLK_ESCAPE
                )
            ))

        while running:
            # This will short-cicuit out renderloop.
            if num_frames > 0 and frames >= (num_frames - 1):
                running = False

            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                if quit_condition(event):
                    running = False

            root.traverse(traversal)

            sdl2.SDL_GL_SwapWindow(self.window)

            frames += 1

        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

        return frames / (time.time() - start)

    def _get_window_size(self):
        w, h = ctypes.c_int(), ctypes.c_int()

        sdl2.SDL_GetWindowSize(self.window, ctypes.byref(w), ctypes.byref(h))

        return w, h

    @property
    def width(self):
        return self._get_window_size()[0].value

    @property
    def height(self):
        return self._get_window_size()[1].value

    @property
    def fullscreen(self):
        return sdl2.SDL_GetWindowFlags(self.window) \
            & sdl2.SDL_WINDOW_FULLSCREEN

    @fullscreen.setter
    def fullscreen(self, fullscreen):
        sdl2.SDL_SetWindowFullscreen(self.window, fullscreen)

    @property
    def title(self):
        return sdl2.SDL_GetWindowTitle(self.window).decode("utf8")

    @title.setter
    def title(self, title):
        sdl2.SDL_SetWindowTitle(self.window, title.encode("utf8"))
