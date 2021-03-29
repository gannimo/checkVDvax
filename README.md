# checkVDvax

Scraper to check the [Corona vaccination page](https://coronavax.unisante.ch/) of
the Canton de Vaud. The web page contains some information about availability in
different regions and eligibility.

The script scrapes the web page and parses both availability of appointments in
different centers and eligibility criteria.

If anything changes, it reports to the console. This script can also be setup as a
cron job.


## Command line parameters:

* `-v` Verbose output (e.g., availability and eligibility criteria or diff), default: false
* `-s` Only print to console if anything chanages (perfect for cron jobs), default: false
* `-f` Local storage/cache of availability/eligiblity/website, default: checkvax.json


## Example

Simple local invocation:

```
$ python3 checkvax.py 
No new eligibility or availibility found.
```

Give some more details:

```
$ python3 checkvax.py
Website has changed, go check out https://coronavax.unisante.ch/
Eligibility:
- Personnes âgées de 65 ans ou plus (nées en 1956 ou avant)
- Résidents et personnel des EMS
- Personnes avec maladie chronique à risque* (et femmes enceintes avec maladie chronique à haut risque*)
- Proches aidants avec carte d'urgence du CMS** ou proches aidants soutenus par un CMS***
- Personnel de santé en contact régulier avec patient·e·s COVID-19 ou patient·e·s particulièrement vulnérables (soins intensifs, soins intermédiaires, services pour patients atteints de COVID-19, urgences)****
- Personnel de santé en contact avec des patients****
Availability:
- Centre CoVID-19 des Pâquis, Morges: Rendez-vous disponibles
- Centre Hospitalier Universitaire Vaudois (CHUV): Rendez-vous disponibles
- Clinique La Lignière: Rendez-vous disponibles
- Hôpital d'Yverdon-les-Bains (eHnv): Rendez-vous disponibles
- Hôpital Intercantonal de la Broye (HIB) - Payerne: Rendez-vous disponibles
```

Check the diff:

```
$ python3 checkvax.py -s
Website has changed, diff: +1 -1 lines.
```

If you want to run the script as `cron` job, you may add the following to your
`crontab`:

```
*/15 *  * * *   USER cd /opt/checkvax && ./checkvax.py -s
```

You'll then receive an email to `USER` whenever the script picks something up.


## Changelog

* 2021-03-29 version 0.4: better documentation and some code refactoring
* 2021-03-26 version 0.3: fancier parsing and storing of data
* 2021-03-25 version 0.2: added new eligibility (65+)
* 2021-03-14 version 0.1: first script with base eligibility (75+)


## Copyright and liability.

Created by `Mathias Payer <mathias.payer@nebelwelt.net>`. If anything breaks, you
get to keep the pieces. Code licensed under Apache/2.
