# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# Exporter file; produces Prometheus metrics using the crawled printer values from ricoh_data_cralwer.py

from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

import ricoh_data_crawler as ricoh

REQUEST_TIME = Summary("ricoh_printer_exporter_collect_",
                       "Time spent to collect metrics from ricoh_data_crawler.py")

class RicohPrinterExporter:
    soups: list
    urls : list

    def __init__(self, soups, urls) -> None:
        self.soups = soups
        self.urls = urls

    @REQUEST_TIME.time()
    def collect(self):

        printer_generator = ricoh.get_printer_values(self.soups, self.urls)

        for printer in printer_generator:

            g = GaugeMetricFamily(
                name='ricoh_printer_level_black',
                documentation='black toner level in percent')
            g.add_metric([printer.printer_name], printer.level_black)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_cyan',
                documentation='cyan toner level in percent')
            g.add_metric([printer.printer_name], printer.level_cyan)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_magenta',
                documentation=',magenta toner level in percent')
            g.add_metric([printer.printer_name], printer.level_magenta)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_yellow',
                documentation='yellow toner level in percent')
            g.add_metric([printer.printer_name], printer.level_yellow)
            yield g