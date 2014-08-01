import sobek
import psutil
import collections


NETWORK_INTERFACE = "em1"


# TODO: This is a retarded hack.
def network_down():
    recv = psutil.network_io_counters(pernic=1)[NETWORK_INTERFACE].bytes_recv

    return (recv / 1000.0) / 1000.0


class StatsCollector(sobek.Callback):
    TIMEOUT = 1.0

    class Stat:
        def __init__(self, callback, average=False, maxlen=10):
            self._values = collections.deque(maxlen=maxlen)
            self._callback = callback
            self._average = average

        @property
        def value(self):
            self._values.append(self._callback())

            if self._average:
                return sum(self._values) / max(len(self._values), 1)

            else:
                return self._values[-1]

    def init(self, node, state):
        self._stats = {
            "cpu": self.Stat(lambda: psutil.cpu_percent(), True, 20),
            "mem": self.Stat(lambda: psutil.virtual_memory().percent),
            "disk": self.Stat(lambda: psutil.disk_usage("/").percent),
            "net": self.Stat(network_down)
        }

    def call(self, node, state):
        for stat_name, stat in self._stats.items():
            node.stats[stat_name] = stat.value

        node.redraw = True
