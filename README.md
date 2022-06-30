# prometheus-ricoh-printer-exporter
Building a prometheus exporter for ricoh-printer related information like toner level

## Export still under development

## Install
You'll be able to install the exporter via pip, but that's still WIP

## Test
(currently you have to clone the Repository to test (s.a.))

To test the exporter, you can host the script on your own machine:
  1. `python3 prometheus_ricoh_printer_exporter/main.py`
  2. (from another terminal) `curl 127.0.0.1:9840`

Running `curl 127.0.0.1:9840` should give you an output of similar structure
like this:
```
# HELP ricoh_printer_level_black black toner level in percent
# TYPE ricoh_printer_level_black gauge
ricoh_printer_level_black 50.0
```
(The output should be similar for other data points, i.e. cyan)

## Usage
```
usage: main.py [-h] [-w LISTENADDRESS | -i]

Set up the Prometheus exporter (connection ports)

options:
  -h, --help            show this help message and exit
  -w LISTENADDRESS, --web.listen-address LISTENADDRESS
                        Address and port to expose metrics and web interface. Default: ":9840" To listen on all interfaces, omit the IP. ":<port>"` To listen on a specific IP: <address>:<port>
  -i, --insecure        Skip SSL validation of the printer website.
```
