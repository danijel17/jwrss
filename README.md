# jwrss

Neslužbeni RSS generator za hrvatsku stranicu JW.org **„Novo na stranici”**
(<https://www.jw.org/hr/sto-je-novo/>).

Skripta dohvaća stranicu, čita popis stavki iz `div.whatsNewItems` (svaka stavka
sadrži datum objave, kategoriju, naslov i poveznicu) te generira RSS 2.0 datoteku
`jw_hr.xml` sa stavkama poredanima od najnovije prema najstarijoj.

## Instalacija

```bash
pip install -r requirements.txt
```

## Pokretanje

```bash
python generate_rss.py
```

Rezultat: datoteka `jw_hr.xml` u istom direktoriju.

## Automatsko osvježavanje (GitHub Actions)

U repozitoriju se nalazi workflow `.github/workflows/rss.yml` koji svakih 30
minuta pokreće skriptu i commita ažurirani `jw_hr.xml`. Možeš ga pokrenuti i
ručno preko kartice **Actions → Generate JW.org HR RSS → Run workflow**.

Feed je tada dostupan na „raw” URL-u, npr.:

```
https://raw.githubusercontent.com/danijel17/jwrss/main/jw_hr.xml
```

Taj URL zalijepi u svoj RSS čitač (Feedly, Thunderbird, NetNewsWire itd.).

Interval možeš promijeniti u `cron` izrazu (preporuka: 15–60 minuta).

## Ostale opcije za raspoređivanje

Umjesto GitHub Actionsa možeš koristiti cron (Linux/Raspberry Pi), Windows Task
Scheduler ili Synology NAS zadatak koji periodički pokreće `python generate_rss.py`.

## Napomena

Ovo je neslužbeni feed i ni na koji način nije povezan s JW.org. Ako se HTML
struktura stranice promijeni, možda će trebati prilagoditi CSS selektore u
`generate_rss.py`.
