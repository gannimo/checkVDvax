#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Mathias Payer <mathias@nebelwelt.net>"
__description__ = "Check vaccination availability and eligibility"

import requests
import urllib.request
from bs4 import BeautifulSoup
from argparse import ArgumentParser
import os
import difflib

URL_VD = 'https://coronavax.unisante.ch/'

OLD_ELIGIBILITY = [
'Personnes âgées de 75 ans ou plus (nées en 1946 ou avant)',
'Résidents et personnel des EMS',
'Personnes avec maladie chronique à haut risque*',
'Personnel de santé en contact régulier avec patient·e·s COVID-19 ou patient·e·s particulièrement vulnérables (soins intensifs, soins intermédiaires, services pour patients atteints de COVID-19, urgences)**',
'Personnes âgées de 65 ans ou plus (nées en 1956 ou avant)',
'Personnes avec maladie chronique à\xa0risque*',
'Proches aidants avec carte d\'urgence de l\'AVASAD ou proches aidants accompagnés par un CMS***'
]

OLD_FILE = 'vdvax.html'

def scrape_page(url = URL_VD):
    # get the page
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print('ERR: Could not get url.')
        raise SystemExit(err)

    return response.text


def check_availability(soup, verbose):
    hosps = soup.find_all('div', class_='hosp')
    res = []
    if verbose:
        print('Checking availabilities:')
    for hosp in hosps:
        name = hosp.find('strong').text
        avail = hosp.find('span')['title']
        if verbose:
            print('- {}: {}'.format(name, avail))
        if avail != 'Complet':
            res.append('{}: {}'.format(name, avail))
    return res


def check_eligibility(soup, verbose):
    avails = soup.find_all(id='vax_groups')
    res = []
    if verbose:
        print('Checking eligibility:')
    for avail in avails:
        for item in avail.find_all('li'):
            if item.text not in OLD_ELIGIBILITY:
                res.append(item.text)
            if verbose:
                print('- {}'.format(item.text))
    return res

def check_diff(html, args):
    if args.diff:
        old = ''
        if os.path.isfile(OLD_FILE):
            with open(OLD_FILE, 'r') as f:
                old = f.read().splitlines()
                f.close()
        diffs = difflib.ndiff(old, html.splitlines())
        added = 0
        removed = 0
        if args.verbose:
            print('Checking for diffs:')
        for line in diffs:
            if line[0] == '+':
                added += 1
            if line[0] == '-':
                removed += 1
            if (line[0] == '+' or line[0] == '-'):
                print(line)

        # Store new file
        if added != 0 or removed != 0:
            print('Webpage has changed, diff: +{} -{} lines.'.format(added, removed))
            print('Go check out {}'.format(URL_VD))
            with open(OLD_FILE, 'w') as f:
                f.write(html)
                f.close()


if __name__ == "__main__":
    parser = ArgumentParser(description=__description__)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, required=False, help='Be a little more verbose.')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', default=False, required=False, help='Only print to console if anything has changed.')
    parser.add_argument('-d', '--diff', dest='diff', action='store_true', default=False, required=False, help='Diff the web page to a local copy (and update if anything has changed). Sanity check if scraping is not perfect.')
    args = parser.parse_args()

    # scrape and parse html
    html = scrape_page()
    soup = BeautifulSoup(html, 'html.parser')

    # check availability and eligibility
    locs = check_availability(soup, args.verbose)
    eligs = check_eligibility(soup, args.verbose)

    if len(eligs) != 0:
        print('Eligibility has changed, go check out {}'.format(URL_VD))
        print('Eligibility:')
        print(eligs)
        print('Availability:')
        print(locs)
    else:
        if not args.verbose and not args.silent:
            print('No new eligibility found, omitting availability.')

    # diff old and new
    check_diff(html, args)


