
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
# STÁHNUTÍ STRÁNKY
def get_soup(url: str) -> BeautifulSoup:
    """Stáhne HTML z URL a vrátí jako BeautifulSoup objekt."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování stránky: {e}")
        sys.exit(1)
