import orodja
import re
import requests
import sys

STEVILO_STRANI = [('a', 9), ('b', 35), ('c', 62), ('d', 6), ('e', 9), ('f', 15), ('g', 19), ('h', 18), ('i', 4), ('j', 4), ('k', 4), ('l', 17), ('m', 22), ('n', 4), ('o', 5), ('p', 39), ('q', 4), ('r', 25), ('s', 67), ('t', 20), ('u', 1), ('v', 11), ('w', 9), ('y', 1), ('z', 1), ('0-9', 1)]
STEVILO_RECEPTOV_NA_STRAN = 24
VSILI_PRENOS = False

for t in STEVILO_STRANI:
    crka = t[0]
    dolzina = t[1]
    st = 1
    for d in range(dolzina):
        url = f'https://www.bbc.co.uk/food/recipes/a-z/{crka}/{d + 1}#featured-content'
        datoteka = f'recepti/zacetne_strani/{crka}.html'
        if st == 1:
            orodja.shrani_spletno_stran(url, datoteka)
            st += 1
        else:
            orodja.shrani_spletno_stran(url, datoteka, zdruzi=datoteka, vsili_prenos=VSILI_PRENOS)