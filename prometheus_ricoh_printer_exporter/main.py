# This file is licensed under the ISC license.
# Oskar Druska 2022
# For further information look up LICENSE.txt

# Exporter entry point; handles URLs and BeautifulSoup objects

import sys
import argparse
import time
import requests
import logging
from bs4 import BeautifulSoup as bs
from prometheus_client import start_http_server, REGISTRY
from . import exporter_file


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    url_oak = "http://oak.inm7.de/web/guest/en/websys/webArch/getStatus.cgi"
    url_pine = "http://pine.inm7.de/web/guest/en/websys/webArch/getStatus.cgi"
    url_willow = "http://willow.inm7.de/web/guest/de/websys/webArch/getStatus.cgi"
    url_larch = "http://larch.inm7.de/web/guest/de/websys/webArch/getStatus.cgi"

    urls = [url_oak, url_pine, url_willow, url_larch]

    args = get_parsed_args()

    try:
        soups = get_soups(urls, args.insecure)
    except ConnectionError as c:  # raised, if request doesn't return HTML code 200
        logging.error(c)
        sys.exit(c.strerror)
    except TimeoutError as t:
        logging.error(t)
        sys.exit(t.strerror)

    logging.info('Cooked soups!')

    REGISTRY.register(exporter_file.RicohPrinterExporter(soups=soups, urls=urls))

    if args.listenaddress is None:
        start_http_server(port=9840, addr='127.0.0.1')
    else:
        ip, port = args.listenaddress.split(":")
        if ip:
            start_http_server(port=int(port), addr=ip)
        else:  # listen on all interfaces
            start_http_server(port=int(port))

    # keep the thing going indefinitely
    logging.info("Exporter started!")
    while True:
        time.sleep(1)


def get_soups(urls: list, insec_bool: bool):
    '''Returns a list containing a soup obejct for each printer in urls.'''

    soups = []

    for url in urls:
        logging.info("Connecting to: " + url + " ...")

        r_url = requests.get(url, verify=not insec_bool)
        if r_url.status_code != 200:
            raise ConnectionError("Something's wrong with the Website:\n" + r_url + "\n" + str(r_url.status_code))
        soups.append(bs(r_url.text, 'html.parser'))

    return soups


def get_parsed_args():
    '''argparser; returns the args from command line'''

    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    mutual_group = parser.add_mutually_exclusive_group()
    mutual_group.add_argument(
        '-w', '--web.listen-address',
        type=str,
        dest='listenaddress',
        help='Address and port to expose metrics and web interface. Default: ":9840"\n'
        'To listen on all interfaces, omit the IP. ":<port>"`\n'
        'To listen on a specific IP: <address>:<port>')
    mutual_group.add_argument(
        '-i', '--insecure',
        dest='insecure',
        action='store_true',
        default=False,
        help='Skip SSL validation of the printer website.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
