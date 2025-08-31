
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
import pandas as pd
import time
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

    table = soup.find("table")
    if not table:
        print("Tabulka s obcemi nebyla nalezena.")
        return []

    for link in table.find_all("a"):
        href = link.get("href", "")
        if "xobec" in href:
            full_url = "https://www.volby.cz/pls/ps2017nss/" + href
            links.append(full_url)

    return links
# -----------------------------------------------------------------------------
# ZÍSKÁNÍ DAT O JEDNÉ OBCI
def get_obec_data(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Název a kód obce
            obec_info = soup.find("h3").text.strip()
            casti = obec_info.replace("Obec:", "").strip().split("(")
            nazev_obce = casti[0].strip()
            kod_obce = casti[1].replace(")", "").strip() if len(casti) > 1 else ""

            # Základní statistiky
            def get_td_text(header):
                td = soup.find("td", {"headers": header})
                return td.text.strip().replace("\xa0", "") if td else ""

            volici = get_td_text("sa2")
            obalky = get_td_text("sa3")
            platne_hlasy = get_td_text("sa6")

            # Hlasy pro strany
            strany = soup.find_all("td", {"class": "overflow_name"})
            hlasy = soup.find_all("td", {"headers": ["t1sb3", "t2sb3"]})

            vysledky_stran = {}
            for i, strana in enumerate(strany):
                nazev_strany = strana.text.strip()
                pocet_hlasu = hlasy[i].text.strip().replace("\xa0", "") if i < len(hlasy) else ""
                vysledky_stran[nazev_strany] = pocet_hlasu

            return {
                "kód obce": kod_obce,
                "název obce": nazev_obce,
                "voliči v seznamu": volici,
                "vydané obálky": obalky,
                "platné hlasy": platne_hlasy,
                **vysledky_stran
            }

        except requests.RequestException as e:
            print(f"Chyba při stahování {url}: {e}")
            if attempt < retries - 1:
                print("Zkusím to znovu za 2 sekundy...")
                time.sleep(2)
            else:
                print("Přeskakuji tuto obec po 3 pokusech.")
                return None

# HLAVNÍ FUNKCE
def main():
    if not validate_args(sys.argv):
        return

    url = sys.argv[1]
    output_file = sys.argv[2]

    print("Stahuji odkazy na obce...")
    obce_links = get_obce_links(url)
    print(f"Nalezeno {len(obce_links)} obcí. Zpracovávám data...")

    data = []
    start_time = time.time()

    for i, link in enumerate(obce_links, start=1):
        obec_data = get_obec_data(link)
        if obec_data:
            data.append(obec_data)

        # průběžný výpis
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = avg_time * (len(obce_links) - i)
        print(f"Zpracováno {i}/{len(obce_links)}: {obec_data['název obce'] if obec_data else 'CHYBA'} | "
              f"čas od začátku: {elapsed:.1f}s | odhad do konce: {remaining:.1f}s")

        time.sleep(0.5)  # pauza mezi obcemi

    # Uložit do CSV až po zpracování všech obcí
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Hotovo! Výsledky uloženy do souboru: {output_file}")

# ------------------------------------------------------------------------------

# SPUŠTĚNÍ
if __name__ == "__main__":
    main()