# Recepti na BBC Food

Analizirala bom recepte na strani [BBC Food](https://www.bbc.co.uk/food).

Za vsak recept bom zajela:
- naslov,
- avtorja,
- oceno,
- število ocenjevalcev,
- vrsto jedi,
- predviden čas priprave in kuhanja ter
- sestavine.

Datoteka `poberi_url_strani.py` deluje tako, da shrani `html`-strani, ki vsebujejo povezavo na posamezne recepte in podatke o vrsti jedi. Potem lahko z datoteko `poberi_podatke.py` shraniš `html`-strani receptov in z `zajem_in_obdelava_strani.py` želene podatke zapišeš v `json` in `csv` datoteke kot je opisano spodaj.

Obdelani podatki se nahajajo v mapi `obdelani-podatki`. Vsi podatki o določenem receptu so v datoteki `recepti.json`. V datoteki `recepti.csv` je možno najti vse podatke o receptu, razen podatka o sestavinah, kateri se posebej nahaja v datoteki `sestavine.csv`, kjer so sestavine vezane na naslov recepta.

### Hipoteze
- Vegetarijanski recepti so slabše ocenjeni,
- Ali obstaja povezava med avtorjem in časom kuhanja njegovih receptov? (če ima kuhar vsaj 10 receptov)
- Najpogosteje uporabljene sestavine so sol, poper, olje in čebula.
