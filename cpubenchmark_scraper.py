import requests
from bs4 import BeautifulSoup

__link = "https://www.cpubenchmark.net/cpu_list.php"


def add_cpu_scores(laptops: list[dict[str, str]], print_progress: bool = True) -> None:
    """Přidá ke všem notebookům v `laptops` informace o jejich CPU benchmark score"""
    cache_dict = {}  # CPU score cache, aby se pro stejný CPU nehledalo vícekrát
    page = requests.get(__link)
    soup = BeautifulSoup(page.text, "html.parser")
    for laptop in laptops:
        cpu_name = laptop["Model procesoru:"].split("(")[0]
        if cpu_name in cache_dict:
            score = cache_dict[cpu_name]
        else:
            a = soup.find(lambda tag:
                          tag.name == "a" and any(cpu_name == word for word in tag.text.replace("-", " ").split()))
            score = "???" if not a else a.parent.parent.find_all("td")[1].text
            cache_dict[cpu_name] = score
        laptop["CPU"] = score
        if print_progress:
            print(end="*")
