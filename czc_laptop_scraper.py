import itertools

import requests
from bs4 import BeautifulSoup

__link_base = ("https://www.czc.cz/notebooky/produkty?razeni=nejlevnejsi&q-first={}"
               "&cena=9990-16000"
               "&velikost-operacni-pameti-gb=16-128")

__parameter_names = ["Operační systém:",
                     "Velikost operační paměti [GB]:",
                     "Typ paměti:",
                     "Kapacita interního úložiště [GB]:",
                     "Model procesoru:",
                     "Baterie:",
                     "Úhlopříčka displeje [\"]:",
                     "Povrch displeje:",
                     "Numerická klávesnice:",
                     "Materiál šasi:",
                     "Kód výrobce:"]


def get_all_laptop_links(print_progress: bool = True) -> list[str]:
    """:return: List odkazů na všechny notebooky odpovídající `__link_base`"""
    result = []
    for i in itertools.count(start=0):  # Projíždět postupně jednotlivé stránky
        page_first_product_n = i * 27  # Každá stránka má maximálně 27 produktů
        link_page = __link_base.format(page_first_product_n)  # Doplnit číslo stránky do __link_base
        page = requests.get(link_page)
        soup = BeautifulSoup(page.text, "html.parser")
        laptop_links = soup.find_all("a", {"class": "tile-link"})
        if not laptop_links:
            break  # Dostali jsme se na stránku s nula produkty (předchozí stránka byla poslední)
        for laptop_link in laptop_links:
            result.append("https://www.czc.cz" + laptop_link["href"])
        if print_progress:
            print(end="*")
    return result


def laptop_links_to_dicts(links: list[str], print_progress: bool = True) -> list[dict[str, str]]:
    """:return: List slovníků pro notebooky z `links` s paramtery `__parameter_names`"""
    dicts = []
    for link in links:
        # Stáhnout stránku s notebookem
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        # Naplnit slovník
        laptop_dict: dict[str, str] = {"link": link}
        price = soup.find("div", {"class": "total-price"}).find("span", {"class": "price-vatin"}).text
        laptop_dict["price"] = price
        for parameter_name in __parameter_names:
            span = soup.find(lambda tag: tag.name == "span" and parameter_name in tag.text)
            parameter_value = span.find_next("b").text if span else "-"
            laptop_dict[parameter_name] = parameter_value
        laptop_dict["CPU"] = "-"
        laptop_dict["heureka"] = "-"
        dicts.append(laptop_dict)
        if print_progress:
            print(end="*")
    return dicts
