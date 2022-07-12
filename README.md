# prometheus-ricoh-printer-exporter
Building a prometheus exporter for ricoh-printer related information like toner level

## Install
You can install the exporter from this repository using the following command:
`pip install git+https://github.com/o-druska/prometheus-ricoh-printer-exporter.git`

## Test
To test the exporter, you can host the script on your own machine:
  1. `prometheus_ricoh_printer_exporter` (make sure you installed via pip)
  2. (from another terminal) `curl 127.0.0.1:9840`

Running `curl 127.0.0.1:9840` should give you an output of similar structure
like this:
```
# HELP ricoh_printer_level_percent black toner level in percent
# TYPE ricoh_printer_level_percent gauge
ricoh_printer_level_percent{color="black",printer_name="oak.inm7.de"} 50.0
```
(The output should be similar for other data points, i.e. cyan)

## Usage
```
usage: prometheus_ricoh_printer_exporter [-h] [-w LISTENADDRESS | -i]

Set up the Prometheus exporter (connection ports)

options:
  -h, --help            show this help message and exit
  -w LISTENADDRESS, --web.listen-address LISTENADDRESS
                        Address and port to expose metrics and web interface. Default: ":9840" To listen on all interfaces, omit the IP. ":<port>"` To listen on a specific IP: <address>:<port>
  -i, --insecure        Skip SSL validation of the printer website.
```
