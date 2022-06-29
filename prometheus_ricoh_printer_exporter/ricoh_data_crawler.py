#!/usr/bin/env python3
# This will be the script that yields the needed information and "talks" to the printers
import requests
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass

@dataclass
class Printer_Values:
    level_black: float
    level_cyan: float
    level_magenta: float
    level_yellow: float

def get_fill_percent(tag):
    SINGLE_GRAPHIC_CONSTANT = 100/160   # Toner level needs to be parsed by examining the amount of graphical elements
                                        # 160 units display 100%, therefore one unit represents 0,625% off toner (100%/160 == 0,635%)
    fill_percent = float(tag['width']) * SINGLE_GRAPHIC_CONSTANT   # tag['width'] is the amount of graphic units (s.a.) displayed
    return fill_percent

def get_printer_values(soups):
    for soup in soups:
        tag_list = soup.find_all("img", class_="ver-algn-m mgn-R5p bdr-1px-666", attrs='width')

        yield Printer_Values(
            level_black = float(get_fill_percent(tag_list[0])),
            level_cyan = float(get_fill_percent(tag_list[1])),
            level_magenta = float(get_fill_percent(tag_list[2])),
            level_yellow = float(get_fill_percent(tag_list[3]))
        )


'''
def test_main():
    url_oak = "http://oak.inm7.de/web/guest/en/websys/webArch/getStatus.cgi"
    r_oak = requests.get(url_oak, verify=False)

    if r_oak.status_code != 200:
        raise ConnectionError("Something's wrong with the Website:\n" + url_oak + "\n" + str(r_oak.status_code))

    soup_oak = bs(r_oak.text, 'html.parser')

    for tag in soup_oak.find_all("img", class_="ver-algn-m mgn-R5p bdr-1px-666", attrs='width'):
        print('html tag: ' + str(tag))
        print('amount graphic units: ' + tag['width'])
        print('corresponding percentage: ' + str(get_fill_percent(tag)))

if __name__ == '__main__':
    test_main()
'''
