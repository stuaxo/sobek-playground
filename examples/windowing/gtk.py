import time

from gi.repository import Gtk, Gdk, GLib, GtkGLExt, GdkGLExt

from . import window


class GtkWindow(window.Window):
    def __init__(self, width, height, **kwargs):
        window.Window.__init__(self, width, height)

        self._frames = 0

        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.glconfig = GdkGLExt.Config.new_by_mode(
            GdkGLExt.ConfigMode.RGB |
            GdkGLExt.ConfigMode.DEPTH |
            GdkGLExt.ConfigMode.DOUBLE
        )

        self.da = Gtk.DrawingArea()

        GtkGLExt.widget_set_gl_capability(
            self.da,
            self.glconfig,
            None,
            True,
            GdkGLExt.RenderType.RGBA_TYPE
        )

        self.da.set_size_request(width, height)

        self.window.set_reallocate_redraws(True)
        self.window.connect("delete_event", Gtk.main_quit)
        self.window.add(self.da)
        self.window.show_all()

        GtkGLExt.widget_begin_gl(self.da)

        self._init(**kwargs)

        GtkGLExt.widget_end_gl(self.da, False)

    def main_loop(self, root, traversal):
        start = time.time()

        def redraw(*args):
            GtkGLExt.widget_begin_gl(self.da)

            root.traverse(traversal)

            GtkGLExt.widget_end_gl(self.da, True)

            self._frames += 1

        def idle(*args):
            window = self.da.get_window()

            window.invalidate_rect(self.da.get_allocation(), False)
            window.process_updates(False)

            return True

        self.da.connect("draw", redraw)

        GLib.timeout_add(
            1000 // 60,
            idle,
            None,
            priority=Gdk.PRIORITY_REDRAW+100
        )

        Gtk.main()

        return self._frames / (time.time() - start)
