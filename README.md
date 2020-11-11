# Recepti na BBC Food

Analizirala bom recepte na strani [BBC Food](https://www.bbc.co.uk/food).

Za vsak recept bom zajela:
- naslov,
- avtorja,
- oceno,
- število ocenjevalcev,
- vrsta jedi,
- predviden čas priprave in kuhanja ter
- sestavine.

Obdelani podatki se nahajajo v mapi `obdelani-podatki`. Vsi podatki o določenem receptu se najdejo v datoteki `recepti.json`. V datoteki `recepti.csv` je možno najti vse podatke o receptu, razen podatka o sestavinah, kateri se posebej nahaja v datoteki `sestavine.csv`, kjer so sestavine vezane na naslov recepta.
 
### Hipoteze
- Ali je recept bolje ocenjen, če je veganski?
- Ali obstaja povezava med kuharjem in časom kuhanja njegovih receptov? (če ima kuhar vsaj 10 receptov)
- Katere sestavine so najpogosteje uporabljene pri receptih z vsaj 15 ocenjevalci?
