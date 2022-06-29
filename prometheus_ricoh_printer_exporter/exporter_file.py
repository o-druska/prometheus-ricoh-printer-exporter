from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily 

import ricoh_data_crawler as ricoh

REQUEST_TIME = Summary("ricoh_printer_exporter_collect_",
                       "Time spent to collect metrics from ricoh_data_crawler.py")

class RicohPrinterExporter:

    @REQUEST_TIME.time()
    def collect(self):

        printer = ricoh.get_printer_values()

        g = GaugeMetricFamily(
            name='ricoh_printer_level_black',
            documentation='black toner level in percent')
        g.add_metric([], printer.level_black)
        yield g

        g = GaugeMetricFamily(
            name='ricoh_printer_level_cyan',
            documentation='cyan toner level in percent')
        g.add_metric([], printer.level_cyan)
        yield g

        g = GaugeMetricFamily(
            name='ricoh_printer_level_magenta',
            documentation=',magenta toner level in percent')
        g.add_metric([], printer.level_magenta)
        yield g

        g = GaugeMetricFamily(
            name='ricoh_printer_level_yellow',
            documentation='yellow toner level in percent')
        g.add_metric([], printer.level_yellow)
        yield g