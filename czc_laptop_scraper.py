import itertools
import sys

import requests
from bs4 import BeautifulSoup

__LINK_BASE = ("https://www.czc.cz/notebooky/produkty?razeni=nejlevnejsi"
               "&q-first={}"
               "&cena={}"
               "&velikost-operacni-pameti-gb=16-128")  # 16 GB RAM hard-coded minimum

__PARAMETER_NAMES = ["Operační systém:",
                     "Velikost operační paměti [GB]:",
                     "Typ paměti:",
                     "Kapacita interního úložiště [GB]:",
                     "Model procesoru:",
                     "Baterie:",
                     "Úhlopříčka displeje [\"]:",
                     "Povrch displeje:",
                     "Numerická klávesnice:",
                     "Materiál šasi:",
                     "Kód výrobce:",
                     "V nabídce od:"]


def get_all_laptop_links(price_range: str, print_progress: bool = True) -> list[str]:
    """:return: List odkazů na všechny notebooky odpovídající `__link_base`"""
    result = []
    for i in itertools.count(start=0):  # Projíždět postupně jednotlivé stránky
        page_first_product_n = i * 27  # Každá stránka má maximálně 27 produktů
        # Doplnit číslo stránky a cenový rozsah do __link_base
        link_page = __LINK_BASE.format(page_first_product_n, price_range)

        page = requests.get(link_page)
        soup = BeautifulSoup(page.text, "html.parser")
        laptop_links = soup.find_all("a", {"class": "tile-link"})
        if not laptop_links:
            break  # Dostali jsme se na stránku s nula produkty (předchozí stránka byla poslední)
        for laptop_link in laptop_links:
            result.append("https://www.czc.cz" + laptop_link["href"])
        if print_progress:
            print(end="*", flush=True)
    return result


def laptop_links_to_dicts(links: list[str], print_progress: bool = True) -> list[dict[str, str]]:
    """:return: List slovníků pro notebooky z `links` s paramtery `__parameter_names`"""
    loading_current = 0
    loading_max = len(links)

    dicts = []
    for link in links:
        # Stáhnout stránku s notebookem
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        # Naplnit slovník
        laptop_dict: dict[str, str] = {"link": link}
        # - Cena
        price = soup.find("div", {"class": "total-price"}).find("span", {"class": "price-vatin"}).text
        laptop_dict["price"] = price
        # - - Případná sleva
        laptop_dict["sleva"] = "-"
        reduced_price = soup.find("span", {"class": "price action"})
        if reduced_price:
            laptop_dict["sleva"] = reduced_price.find("span", {"class": "price-vatin"}).text
        # - Vybrané parametry
        for parameter_name in __PARAMETER_NAMES:
            span = soup.find(lambda tag: tag.name == "span" and parameter_name in tag.text)
            parameter_value = span.find_next("b").text if span else "-"
            laptop_dict[parameter_name] = parameter_value
        # - CPUBenchmark skóre :: zatím prázdné a může být doplněno po spuštění příkazu 2
        laptop_dict["CPU"] = "-"
        # - Odkaz na Heureka :: pouze vyhledání kódu výrobce
        laptop_dict["heureka"] = f"https://www.heureka.cz/?h%5Bfraze%5D={laptop_dict['Kód výrobce:']}"
        dicts.append(laptop_dict)
        if print_progress:
            loading_current += 1
            sys.stdout.write(f"\r[{loading_current}/{loading_max}]")
    return dicts
