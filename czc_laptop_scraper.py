import itertools

import requests
from bs4 import BeautifulSoup

from models import Laptop

__link_base = ("https://www.czc.cz/notebooky/produkty?razeni=nejlevnejsi&q-first={}"
               "&cena=9990-16000"
               "&velikost-operacni-pameti-gb=16-128")


def get_all_laptop_links() -> list[str]:
    """:returns: List odkazů na všechny notebooky odpovídající __link_base"""
    result = []
    for i in itertools.count(start=0):  # Projíždět postupně jednotlivé stránky
        page_first_product_n = i * 27  # Každá stránka má maximálně 27 produktů
        link_page = __link_base.format(page_first_product_n)
        page = requests.get(link_page)
        soup = BeautifulSoup(page.text, "html.parser")
        laptop_links = soup.find_all("a", {"class": "tile-link"})
        if not laptop_links:
            break  # Dostali jsme se na stránku s nula produkty
        for laptop_link in laptop_links:
            result.append("https://www.czc.cz/" + laptop_link["href"])
    return result


def udelej_neco_s_linkama(links: list[str]) -> None:
    for link in links:
        laptop = Laptop(link=link)
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        stat_os = soup.find(lambda tag: tag.name == "span" and "Operační systém:" in tag.text).find_next("b").text
        print(stat_os)
        stat_ram_ngbs = soup.find(lambda tag: tag.name == "span" and "Velikost operační paměti [GB]:" in tag.text).find_next("b").text
        print(stat_ram_ngbs)
        stat_ram_type = soup.find(lambda tag: tag.name == "span" and "Typ paměti:" in tag.text).find_next("b").text
        print(stat_ram_type)


if __name__ == "__main__":
    udelej_neco_s_linkama(["https://www.czc.cz/acer-aspire-3-a315-59-stribrna/361988/produkt"])
