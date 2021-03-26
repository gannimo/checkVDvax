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
import json

URL_VD = 'https://coronavax.unisante.ch/'

def scrape_page(url = URL_VD):
    # get the page
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print('ERR: Could not get url.')
        raise SystemExit(err)

    return response.text


def find_availability(soup):
    hosps = soup.find_all('div', class_='hosp')
    res = {}
    #if verbose:
    #    print('Checking availabilities:')
    for hosp in hosps:
        name = hosp.find('strong').text
        avail = hosp.find('span')['title']
        #if verbose:
        #    print('- {}: {}'.format(name, avail))
        #if avail != 'Complet':
        #    res.append('{}: {}'.format(name, avail))
        res[name] = avail
    return res


def check_availibility(avails, old_avails):
    for name in avails:
        if name in old_avails:
            if old_avails[name] != avails[name]:
                return True
        else:
            return True
    return False


def find_eligibility(soup):
    avails = soup.find_all(id='vax_groups')
    res = []
    #if verbose:
    #    print('Checking eligibility:')
    for avail in avails:
        for item in avail.find_all('li'):
            #if item.text not in OLD_ELIGIBILITY:
            res.append(item.text)
            #if verbose:
            #    print('- {}'.format(item.text))
    return res


def check_eligibility(eligs, old_eligs):
    for name in eligs:
        if name not in old_eligs:
            return True
    return False


def check_diff(html, old_html):
    diffs = difflib.ndiff(old_html, html.splitlines())
    added = 0
    removed = 0
    res = []
    for line in diffs:
        if line[0] == '+':
            added += 1
        if line[0] == '-':
            removed += 1
        if (line[0] == '+' or line[0] == '-'):
            res.append(line)
    return (added, removed, res)


if __name__ == "__main__":
    parser = ArgumentParser(description=__description__)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, required=False, help='Be a little more verbose.')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', default=False, required=False, help='Only print to console if anything has changed.')
    parser.add_argument('-f', '--file', dest='file', default='checkvax.json', required=False, help='Filename to load/store checkvax data (default: "checkvax.json").')
    args = parser.parse_args()

    # load dumped data
    if os.path.isfile(args.file):
        with open(args.file, 'r') as f:
            dump = json.load(f)
            f.close()    
    else:
        dump = {}
        dump['html'] = ''
        dump['eligibility'] = []
        dump['availability'] = {}

    # scrape and parse html
    html = scrape_page()
    soup = BeautifulSoup(html, 'html.parser')

    # check availability and eligibility
    avails = find_availability(soup)
    eligs = find_eligibility(soup)

    # Check if anything has changed (at a semantic level)
    if check_availibility(avails, dump['availability']) or check_eligibility(eligs, dump['eligibility']):
        print('Eligibility/availability has changed, go check out {}'.format(URL_VD))
        print('Eligibility:')
        # Print any new eligibility
        for elig in eligs:
            if elig not in dump['eligibility']:
                print('- {}'.format(elig))
        # print any new availability
        print('Availability:')
        for name in avails:
            if avails[name] != 'Complet':
                print('- {}: {}'.format(name, avails[name]))
    else:
        if not args.silent:
            print('No new eligibility or availibility found.')

    dump['availability'] = avails
    dump['eligibility'] = eligs

    # Check if anything has changed (at a syntactic level)
    # diff old and new
    (added, removed, res) = check_diff(html, dump['html'])
    dump['html'] = html.splitlines()
    if args.verbose and (added != 0 or removed != 0):
        print('Dumping website diff ({} added {} removed):'.format(added, removed))
        for line in res:
            print(line)

    with open(args.file, 'w') as f:
        json.dump(dump, f)
        f.close()    
