import sobek
import sobek.cairo as cairo


class StatsWidget(sobek.Widget):
    DEFAULT_OPTIONS = {
        "title-bg": (0.0, 0.0, 0.0),
        "title-fg": (1.0, 1.0, 1.0),
        "stat-bg": (0.0, 0.0, 0.0),
        "stat-name-fg": (1.0, 1.0, 1.0),
        "stat-val-fg": (0.0, 0.0, 0.0),
        "stat-progress-bg": (0.6, 0.6, 0.6),
        "stat-progress-fg-low": (0.0, 0.8, 0.0),
        "stat-progress-fg-med": (0.8, 0.8, 0.0),
        "stat-progress-fg-hi": (0.8, 0.0, 0.0),
        "font": "Sans",
        "font-size": 0.5,
        "font-weight": cairo.FONT_WEIGHT_NORMAL,
        "font-slant": cairo.FONT_SLANT_NORMAL,
        "title": "system",
        "title-width-scale": 3.0,
        "progress-size": 4.0,
        "arrow-size": 0.25
    }

    def __init__(self):
        sobek.Widget.__init__(self)

        self.options = {}
        self.stats = {}
        self.statics = {}

    def _statbar_path(self, cr, x, w, arsz, left=True, right=True):
        cr.save()

        cr.translate(x, 0.0)
        cr.move_to(0.0, 0.0)

        if left:
            cr.line_to(arsz, 0.5)

        cr.line_to(0.0, 1.0)

        if right:
            cr.line_to(w - arsz, 1.0)
            cr.line_to(w, 0.5)
            cr.line_to(w - arsz, 0.0)

        else:
            cr.line_to(w, 1.0)
            cr.line_to(w, 0.0)

        cr.close_path()
        cr.restore()

    def _statbar(self, cr, x, w, arsz, left=True, right=True):
        self._statbar_path(cr, x, w, arsz, left, right)

        cr.fill()

    def _statbar_progress(
        self,
        cr,
        x,
        w,
        pw,
        p,
        options,
        left=True,
        right=True
    ):
        cr.save()

        arsz = options["arrow-size"]

        self._statbar_path(cr, x, w + pw, arsz, left, right)

        cr.clip()
        cr.set_antialias(cairo.ANTIALIAS_NONE)
        cr.set_source_rgb(*options["stat-progress-bg"])
        cr.rectangle(x, 0.0, w + pw, 1.0)
        cr.fill()
        cr.set_antialias(cairo.ANTIALIAS_DEFAULT)

        def progress_slant(xx):
            cr.move_to(xx, 1.0)
            cr.line_to(xx + (options["arrow-size"] * 2.0), 0.0)
            cr.line_to(xx, 0.0)
            cr.close_path()
            cr.fill()

        if p < 33.3:
            cr.set_source_rgb(*options["stat-progress-fg-low"])

        elif p < 66.6:
            cr.set_source_rgb(*options["stat-progress-fg-med"])

        else:
            cr.set_source_rgb(*options["stat-progress-fg-hi"])

        pct = pw * (p / 100.0)

        cr.rectangle(x + w, 0.0, pct, 1.0)
        cr.fill()

        progress_slant(x + w + pct)

        cr.set_line_width(0.2)
        cr.set_source_rgb(*options["stat-bg"])
        cr.rectangle(x, 0.0, w, 1.0)
        cr.fill()

        progress_slant(x + w - 0.05)

        self._statbar_path(cr, x, w + pw, arsz, left, right)

        cr.stroke()
        cr.restore()

    def draw_widget(self, cr, state):
        opts = self.DEFAULT_OPTIONS.copy()

        opts.update(self.options)

        # Clear the texture.
        cr.save()
        cr.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.restore()

        sw, sh = self.width, self.height

        # cr.save()

        cr.scale(sh, sh)
        # The following would invert the drawing, rather than requiring the
        # shader itself to do the inversion.
        # cr.translate(0.0, 1.0)
        # cr.scale(1.0, -1.0)

        # The size of each stat area is determined by the text within.
        cr.select_font_face(
            opts["font"],
            opts["font-slant"],
            opts["font-weight"]
        )

        cr.set_font_size(opts["font-size"])

        exb, eyb, ew, eh, exa, eya = cr.text_extents(opts["title"])

        tw = ew * opts["title-width-scale"]

        # Draw the first arrow/title thingy.
        cr.set_source_rgb(*opts["title-bg"])

        self._statbar(cr, 0.0, tw, opts["arrow-size"], False)

        cr.save()
        cr.translate((tw - ew) / 2.0, ((1.0 - eh) / 2.0) - eyb)
        cr.set_source_rgb(*opts["title-fg"])
        cr.show_text(opts["title"])
        cr.fill()
        cr.restore()

        # This is our "item-x" value, which determines the x-offset of the
        # next stat display region.
        ix = tw

        # Now, we need to render each stat, sorted by their key values.
        for key, val in sorted(self.stats.items()):
            exb, eyb, ew, eh, exa, eya = cr.text_extents(key)
            arsz = opts["arrow-size"]
            pw = opts["progress-size"]
            iw = (ew + (arsz * 3.0))

            self._statbar_progress(cr, ix, iw, pw, val, opts)

            cr.set_source_rgb(*opts["stat-name-fg"])

            # The state name.
            cr.save()
            cr.translate(ix + (arsz * 2.0), ((1.0 - eh) / 2.0) - eyb)
            cr.show_text(key)
            cr.fill()
            cr.restore()

            cr.set_source_rgb(*opts["stat-val-fg"])

            # The stat value.
            strval = "%.01f%%" % val

            exb, eyb, ew, eh, exa, eya = cr.text_extents(strval)

            offset = (pw - ew) / 2.0

            cr.save()
            cr.translate(
                ix + (arsz * 2.0) + iw + offset,
                ((1.0 - eh) / 2.0) - eyb
            )

            cr.show_text(strval)
            cr.fill()
            cr.restore()

            ix += iw + pw

        # Now, we need to render each static value, with no progress.
        for val in self.statics.values():
            exb, eyb, ew, eh, exa, eya = cr.text_extents(val)
            arsz = opts["arrow-size"]
            iw = ew + (arsz * 4.0)

            cr.set_source_rgb(*opts["stat-bg"])

            self._statbar(cr, ix, iw, arsz)

            cr.set_source_rgb(*opts["stat-name-fg"])

            # The state name.
            cr.save()
            cr.translate(ix + (arsz * 2.0), ((1.0 - eh) / 2.0) - eyb)
            cr.show_text(val)
            cr.fill()
            cr.restore()

            ix += iw

        """
        cr.restore()

        cr.set_line_width(1.0)
        cr.set_source_rgb(1.0, 0.0, 0.0)
        cr.move_to(0.0, 16.5)
        cr.line_to(1280.0, 16.5)
        cr.stroke()
        """
