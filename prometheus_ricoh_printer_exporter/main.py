import sys
import argparse
import time
from urllib import request
import requests 
from prometheus_client import start_http_server, REGISTRY
import exporter_file
from bs4 import BeautifulSoup as bs

def main():
    args = get_parsed_args()

    try:
        REGISTRY.register(exporter_file.RicohPrinterExporter())
    except ConnectionError as c:
        sys.exit(c.strerror)
    
    if args.listenaddress is None:
        start_http_server(port=9840, addr='127.0.0.1')
    else:
        ip, port = args.listenaddress.split(":")
        if ip:
            start_http_server(port=int(port), addr=ip)
        else:  # listen on all interfaces
            start_http_server(port=int(port))

    # keep the thing going indefinitely
    while True:
        time.sleep(1)

def get_soups(insec_bool):
    url_oak = "http://oak.inm7.de/web/guest/en/websys/webArch/getStatus.cgi"
    url_pine = "http://pine.inm7.de/web/guest/en/websys/webArch/getStatus.cgi"
    url_willow = "http://willow.inm7.de/web/guest/de/websys/webArch/getStatus.cgi"
    url_larch = "http://larch.inm7.de/web/guest/de/websys/webArch/getStatus.cgi"

    urls = [url_oak, url_pine, url_willow, url_larch]
    soups = []

    for url in urls:
        r_url = requests.get(url, verify = not insec_bool)
        if r_url.status_code != 200:
            raise ConnectionError("Something's wrong with the Website:\n" + url_oak + "\n" + str(r_url.status_code))
        soups.append(bs(r_url.text, 'html.parser'))

    return soups


def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Set up the Prometheus exporter (connection ports)')
    mutual_group = parser.add_mutually_exclusive_group()
    mutual_group.add_argument(
        '-w', '--web.listen-address',
        type=str,
        dest='listenaddress',
        help='Address and port to expose metrics and web interface. Default: ":9840"\n'
                'To listen on all interfaces, omit the IP. ":<port>"`\n'\
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