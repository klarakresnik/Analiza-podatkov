import re
import orodja

STEVILO_STRANI = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', '0-9']

vzorec = r'"(https://www.bbc.co.uk(/food/recipes/.*?_\d+?))"'
for crka in STEVILO_STRANI:
    datoteka_zacetne_strani = f'recepti/zacetne_strani/{crka}.html'
    vsebina = orodja.vsebina_datoteke(datoteka_zacetne_strani)
    a = 0
    for zadetek in re.finditer(vzorec, vsebina):
        a += 1
        datoteka_recepta = f'recepti/stran_receptov/{crka}/{a}.html'
        url = zadetek.group(1)
        orodja.shrani_spletno_stran(url, datoteka_recepta)
        isci = zadetek.group(2) + r'.+?<span class="promo__type gel-minion.*?">(?P<zvrst>.+?)</span>'
        pattern = re.compile(
            isci,
            re.DOTALL
            )
        id = zadetek.group(3)
        zvrst = re.search(pattern, vsebina).group(1)
        with open(datoteka_recepta, 'a', encoding='utf-8') as f:
            zvrst = '§' + zvrst + '§'
            f.write(zvrst)