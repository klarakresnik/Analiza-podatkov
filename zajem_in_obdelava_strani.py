import re
import os
import orodja

STEVILKE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
STEVILO_STRANI = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z', '0-9']


vzorec_recepta = re.compile(
    r'<h1 class="gel-trafalgar content-title__text">(?P<naslov>.*?)</h1>.*?' # naslov
    r'<a class="chef__link" href="/food/chefs.*?">(?P<avtor>.+?)</a>.*?' # avtor
    r'recipe-leading-info__side-bar.*?content=".*?">(?P<cas_priprave>.*?)<.*?' # cas priprave
    r'<div class="recipe-ingredients-wrapper"><h2 class="recipe-ingredients__heading gel-double-pica">Ingredients</h2>(?P<sestavine>.+?)</div>.*?' #sestavine
    r'"rating":{"total":(?P<stevilo_ocenjevalcev>.+?),"value":(?P<ocena>.+?)}', # stevilo ocenjevalcev in ocena
    re.DOTALL
)

vzorec_zvrsti = re.compile(
    r'§(?P<zvrst>.+?)§', # zvrst
    re.DOTALL
)

vzorec_avtorja = re.compile(
    r'<a class="chef__link" href="/food/chefs.*?">(?P<avtor>.+?)</a>', # avtor
    re.DOTALL
)

vzorec_casa_kuhanja = re.compile(
    r'<p class="recipe-metadata__cook-time" content=".*?">(?P<cas_kuhanja>.*?)</p>.*?', # cas kuhanja
    re.DOTALL
)

vzorec_diete = re.compile(
    r'">Dietary</p>.*?class="recipe-metadata__.+?">(?P<dieta>Vegetarian)</p></a></div></div>', # dieta
    re.DOTALL
)

vzorec_sestavine = re.compile(
    r'<li class="recipe-ingredients__list-item">.*?<a href="/food/.*?" class="recipe-ingredients__link">(?P<sestavina>.+?)s?</a>.*?</li>', # ena sestavina
    re.DOTALL
)

def uredi_sestavine(niz):
    koncnica = ['gras', 'cres', ' bas']
    sestavine = set()
    for sestavina in vzorec_sestavine.finditer(niz):
        sestavine.add(sestavina.groupdict()['sestavina'])
    return list(sestavine)

def uredi_cas(niz):
    cas = ''
    prva_stevilka = 0
    druga_stevilka = 0
    niz = niz.split(' ')
    for beseda in niz:
        if beseda[0] in STEVILKE:
            if '-' in beseda:
                x = beseda.split('-')
                druga_stevilka = int(x[0])
                prva_stevilka = int(x[1])
            else:
                prva_stevilka = int(beseda)
        else:
            if 'min' in beseda:
                if druga_stevilka == 0:
                    cas += str(prva_stevilka)
                    prva_stevilka = 0
                else:
                    cas += str(druga_stevilka) + '-' + str(prva_stevilka)
                    druga_stevilka = 0
                    prva_stevilka = 0
            if 'hour' in beseda:
                if druga_stevilka == 0:
                    cas += str(prva_stevilka * 60)
                    prva_stevilka = 0
                else:
                    cas += str(druga_stevilka * 60) + '-' + str(prva_stevilka * 60)
                    druga_stevilka = 0
                    prva_stevilka = 0
            if beseda == 'to':
                if prva_stevilka != 0:
                    druga_stevilka = prva_stevilka
                else:
                    cas += '-'
            if beseda == 'less':
                cas += '0'
            if beseda == 'than':
                cas += '-'
            if 'required' == beseda:
                cas = '0-0'
            if beseda == 'over':
                cas += '00-'
            if beseda == 'overnight':
                cas = 'overnight'
    return cas

def uredi_zvrst(niz):
    koncen_niz = ''
    sez_besed = niz.split(' ')
    for beseda in sez_besed:
        if beseda == 'recipe':
            return 'Recipe'
        else:
            if beseda == '&amp;':
                koncen_niz += 'and '
            else:
                koncen_niz += beseda
                if sez_besed.index(beseda) != len(sez_besed)  - 1:
                    koncen_niz += ' '
    return koncen_niz

def uredi_oceno(ocena):
    return round(ocena, 2)

def izloci_podatke_recepta(blok):
    recept = vzorec_recepta.search(blok).groupdict()
    if vzorec_casa_kuhanja.search(blok):
        cas_kuhanja = vzorec_casa_kuhanja.search(blok).groupdict()
        recept['cas_kuhanja'] = uredi_cas(cas_kuhanja['cas_kuhanja'])
    else:
        recept['cas_kuhanja'] = '0'
    recept['cas_priprave'] = uredi_cas(recept['cas_priprave'])
    recept['sestavine'] = uredi_sestavine(recept['sestavine'])
    recept['ocena'] = uredi_oceno(float(recept['ocena']))
    recept['stevilo_ocenjevalcev'] = int(recept['stevilo_ocenjevalcev'])
    zvrst = vzorec_zvrsti.search(blok).groupdict()
    if vzorec_diete.search(blok):
        dieta = vzorec_diete.search(blok).groupdict()
        recept['dieta'] = dieta['dieta']
    else:
        recept['dieta'] = '0'
    recept['zvrst'] = uredi_zvrst(zvrst['zvrst'])
    if recept['cas_priprave'] == None:
        recept['cas_priprave'] = '0'
    return recept

def izloci_sestavine(recepti):
    sestavine = []
    for recept in recepti:
        for sestavina in recept.pop('sestavine'):
            sestavine.append({'recept' : recept['naslov'], 'sestavina' : sestavina})
    return sestavine

recepti = []
for crka in STEVILO_STRANI:
    print(crka)
    for datoteka in os.listdir('recepti/stran_receptov/' + crka):
        with open('recepti/stran_receptov/' + crka + '/' + datoteka, 'r', encoding='utf-8') as f:
            blok = f.read()
            recept = izloci_podatke_recepta(blok)
            recepti.append(recept)
recepti.sort(key=lambda recepti: recepti['naslov'])
orodja.zapisi_json(recepti, 'obdelani-podatki/recepti.json')

sestavine = izloci_sestavine(recepti)
orodja.zapisi_csv(
    recepti,
    ['naslov', 'avtor', 'cas_priprave', 'cas_kuhanja', 'stevilo_ocenjevalcev', 'ocena', 'dieta', 'zvrst'], 'obdelani-podatki/recepti.csv'
)
orodja.zapisi_csv(sestavine, ['recept', 'sestavina'], 'obdelani-podatki/sestavine.csv')