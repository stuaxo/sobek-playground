from . widget import StatsWidget
from . collector import StatsCollector

import sobek


class StatsBar(sobek.Transform):
    def __init__(self):
        sobek.Transform.__init__(self)

        sw = StatsWidget()

        sw.options = {
            "title": "/// STATSBAR",
            "font": "Cantarell",
            "font-size": 0.5,
            "title-width-scale": 1.5,
            "progress-size": 4.0,
            "arrow-size": 0.35
        }

        sw.resize(1280, 30)
        sw.callbacks.append(StatsCollector())

        self.append(sw)

    """
    def update(self, statsbar):
        for stat, stat_key in zip(
            ("cpu", "memory", "disk"),
            ("CPU", "MEM", "HDD")
        ):
            statsbar.texture.stats[stat_key] = \
                statsbar.collector.stats[stat].value

        statsbar.texture.statics["NET"] = \
            "NET %.02fMB" % statsbar.collector.stats["net"].value
    """
