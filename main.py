
# HLAVIČKA PROJEKTU
"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Patricie Hermanová
email: patriciehermanova@gmail.com
"""
# -----------------------------------------------------------------------------

# Oddělovač
oddelovac = "-" * 50

################################### KÓD #######################################

# IMPORT KNIHOVEN
import sys
import requests
from bs4 import BeautifulSoup
import pandas
# -----------------------------------------------------------------------------
# VALIDACE ARGUMENTŮ
def validate_args(args):
    """Zkontroluje platnost argumentů."""
    if len(args) != 3:
        print("Chyba: Musíš zadat 2 argumenty (URL a CSV soubor).")
        return False
    url = args[1]
    if not url.startswith("http"):
        print("Chyba: První argument musí být platný URL odkaz.")
        return False
    return True
# -----------------------------------------------------------------------------
# ZÍSKÁNÍ ODKAZŮ NA OBCE
def get_obce_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Chyba při stahování stránky:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    
    # odkazy na obce jsou ve sloupci "číslo" (odkaz <a>)
    for link in soup.find_all("a"):
        if "xobec" in link.get("href", ""):
            full_url = "https://www.volby.cz/pls/ps2017nss/" + link["href"]
            links.append(full_url)

    return links
# -----------------------------------------------------------------------------
# ZÍSKÁNÍ DAT O JEDNÉ OBCI
def get_obec_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Chyba při stahování stránky:", response.status_code)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Název a kód obce
    obec_info = soup.find("h3").text.strip()  # např. "Obec: Benešov (529303)"
    # Rozdělit podle dvojtečky a závorky
    casti = obec_info.replace("Obec:", "").strip().split("(")
    nazev_obce = casti[0].strip()
    kod_obce = casti[1].replace(")", "").strip()

    # Základní statistiky
    volici = soup.find("td", {"headers": "sa2"}).text.strip().replace("\xa0", "")
    obalky = soup.find("td", {"headers": "sa3"}).text.strip().replace("\xa0", "")
    platne_hlasy = soup.find("td", {"headers": "sa6"}).text.strip().replace("\xa0", "")

    # Hlasy pro strany
    strany = soup.find_all("td", {"class": "overflow_name"})
    hlasy = soup.find_all("td", {"headers": ["t1sb3", "t2sb3"]})

    vysledky_stran = {}
    for i, strana in enumerate(strany):
        nazev_strany = strana.text.strip()
        pocet_hlasu = hlasy[i].text.strip().replace("\xa0", "")
        vysledky_stran[nazev_strany] = pocet_hlasu

    # Vrátíme jako slovník
    return {
        "kód obce": kod_obce,
        "název obce": nazev_obce,
        "voliči v seznamu": volici,
        "vydané obálky": obalky,
        "platné hlasy": platne_hlasy,
        **vysledky_stran
    }

obec_url = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xobec=532771&xvyber=2101"
data = get_obec_data(obec_url)
print(data)
 
        
