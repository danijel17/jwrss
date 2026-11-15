# jwrss

> **⚠️ Zastarjelo / Deprecated.** Koristi **službeni RSS feed** JW.org-a (vidi
> dolje). Ovaj scraper više nije potreban i nije u aktivnoj upotrebi.

## ✅ Preporučeno: službeni JW.org RSS feed

JW.org objavljuje vlastiti službeni RSS feed za „Novo na stranici” — uključuje
kategoriju, naslov, poveznicu, datum objave i sličicu. Održava ga JW.org, uvijek
je ažuran i dostupan je i s „cloud” IP adresa (RSS čitači ga normalno dohvaćaju).

**Hrvatski:**

```
https://www.jw.org/hr/sto-je-novo/rss/WhatsNewWebArticles/feed.xml
```

**Engleski:**

```
https://www.jw.org/en/whats-new/rss/WhatsNewWebArticles/feed.xml
```

Zalijepi URL izravno u svoj RSS čitač (npr. Feeder na Androidu). Nije potrebna
nikakva automatizacija, poslužitelj ni GitHub Actions.

---

## Povijest: neslužbeni scraper (više se ne koristi)

Ranije je ovaj repozitorij sadržavao scraper koji je dohvaćao stranicu
<https://www.jw.org/hr/sto-je-novo/> i generirao `jw_hr.xml`.

**Zašto je napušten:** JW.org je počeo posluživati **praznu stranicu za
podatkovne/„cloud” IP adrese** (npr. GitHub Actions runnere), pa je scraper
pronalazio nula članaka i workflow je padao. Scraping s kućne IP adrese i dalje
radi, ali se oslanja na nestabilne CSS selektore. Budući da postoji službeni
feed, scraper je nepotreban.

Zakazani (cron) workflow je onemogućen; `.github/workflows/rss.yml` se može
pokrenuti još samo ručno (`workflow_dispatch`) za potrebe testiranja.

### Pokretanje scrapera ručno (opcionalno)

```bash
pip install -r requirements.txt
python generate_rss.py   # stvara jw_hr.xml (radi samo s kućne IP adrese)
```

## Napomena

Službeni feed održava JW.org. Scraper je bio neslužbeni i ni na koji način nije
povezan s JW.org.
