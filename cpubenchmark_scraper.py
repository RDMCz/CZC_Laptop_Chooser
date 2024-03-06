import json

import requests
from bs4 import BeautifulSoup

__link = "https://www.cpubenchmark.net/cpu_list.php"


def get_all_cpu_scores(laptops: list[dict[str, str]]):
    cache_dict = {}
    page = requests.get(__link)
    soup = BeautifulSoup(page.text, "html.parser")
    for laptop in laptops:
        cpu_name = laptop["Model procesoru:"].split("(")[0]
        if cpu_name in cache_dict:
            pass
        else:
            a = soup.find(lambda tag:
                          tag.name == "a" and any(cpu_name == word for word in tag.text.replace("-", " ").split()))
            # TODO


if __name__ == "__main__":
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    get_all_cpu_scores(data)
