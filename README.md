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
* `-d` Diff a local copy of the page with the current homepage, default: false


## Example

Simple local invocation:

```
$ python3 checkvax.py 
No new eligibility found, omitting availability.
```

Give some more details:

```
$ python3 checkvax.py -v
Checking availabilities:
- Hôpital Intercantonal de la Broye (HIB) - Payerne: Rendez-vous disponibles
- Centre CoVID-19 des Pâquis, Morges: Complet
- Centre Hospitalier Universitaire Vaudois (CHUV): Complet
- Clinique La Lignière: Complet
- Hôpital d'Yverdon-les-Bains (eHnv): Complet
- Hôpital Riviera-Chablais (HRC) - Rennaz: Complet
Checking eligibility:
- Personnes âgées de 75 ans ou plus (nées en 1946 ou avant)
- Résidents et personnel des EMS
- Personnes avec maladie chronique à haut risque*
- Personnel de santé en contact régulier avec patient·e·s COVID-19 ou patient·e·s
  particulièrement vulnérables (soins intensifs, soins intermédiaires, services pour
patients atteints de COVID-19, urgences)**
```

Check the diff:

```
$ python3 checkvax.py -d -s
Webpage has changed, diff: +1 -1 lines.
```

If you want to run the script as `cron` job, you may add the following to your
`crontab`:

```
*/15 *  * * *   USER cd /opt/checkvax && ./checkvax.py -s -d
```

You'll then receive an email to `USER` whenever the script picks something up.


## Changelog

* 2021-03-25 version 0.2: added new eligibility (65+)
* 2021-03-14 version 0.1: first script with base eligibility (75+)


## Copyright and liability.

Created by `Mathias Payer <mathias.payer@nebelwelt.net>`. If anything breaks, you
get to keep the pieces. Code licensed under Apache/2.
