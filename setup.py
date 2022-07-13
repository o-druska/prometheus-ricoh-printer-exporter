#!/usr/bin/env python3
''' setup file for installation of ricoh printer prometheus exporter '''
from setuptools import setup, find_packages

setup(
    name='prometheus_ricoh_printer_exporter',
    version='1.0.0',
    description='prometheus exporter for printer status for INM7s Ricoh printers',
    author='Oskar Druska',
    author_email='o.druska@fz-juelich.de',
    packages=find_packages(),
    license='ISC',
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'prometheus_client'
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'prometheus_ricoh_printer_exporter=prometheus_ricoh_printer_exporter.main:main'
        ],
    },

)