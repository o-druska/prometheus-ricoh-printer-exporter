# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# Exporter file; produces Prometheus metrics using the crawled printer values from ricoh_data_cralwer.py

from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily

from . import ricoh_data_crawler as ricoh

REQUEST_TIME = Summary("ricoh_printer_exporter_collect_",
                       "Time spent to collect metrics from ricoh_data_crawler.py")


class RicohPrinterExporter:
    soups: list
    urls: list

    def __init__(self, soups, urls) -> None:
        self.soups = soups
        self.urls = urls

    @REQUEST_TIME.time()
    def collect(self):

        printer_generator = ricoh.get_printer_values(self.soups, self.urls)  # returns a Printer_Values object in each generator call

        for printer in printer_generator:
            labels = ['printer_name', 'color']

            g = GaugeMetricFamily(
                name='ricoh_printer_level_percent',
                labels=labels,
                documentation='black toner level in percent')
            g.add_metric([printer.printer_name, 'black'], printer.level_black)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_percent',
                labels=labels,
                documentation='cyan toner level in percent')
            g.add_metric([printer.printer_name, 'cyan'], printer.level_cyan)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_percent',
                labels=labels,
                documentation='magenta toner level in percent')
            g.add_metric([printer.printer_name, 'magenta'], printer.level_magenta)
            yield g

            g = GaugeMetricFamily(
                name='ricoh_printer_level_percent',
                labels=labels,
                documentation='yellow toner level in percent')
            g.add_metric([printer.printer_name, 'yellow'], printer.level_yellow)
            yield g
