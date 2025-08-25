#------------------------------------------------------------------------------

# HLAVIČKA PROJEKTU
"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Patricie Hermanová
email: patriciehermanova@gmail.com
"""
#------------------------------------------------------------------------------

# ZADÁNÍ PROJEKTU

#------------------------------------------------------------------------------

# Oddělovač
oddelovac = "-" * 50

################################### KÓD #######################################

# IMPORT KNIHOVEN
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# VALIDACE ARGUMENTŮ
def validate_args(args):
    if len(args) != 3:
        print("Chyba: Musíš zadat 2 argumenty (URL a CSV soubor).")
        return False
    url = args[1]
    if not url.startswith("http"):
        print("Chyba: První argument musí být platný URL odkaz.")
        return False
    return True

# STÁHNUTÍ STRÁNKY
