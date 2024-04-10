import json
import pathlib
from typing import Optional

import xlsxwriter

import cpubenchmark_scraper as cpu
import czc_laptop_scraper as czc
import input_parser as ip

__PATH = pathlib.Path(__file__).parent
__LAPTOPS_JSON = __PATH / "laptops.json"
__LAPTOPS_XCEL = __PATH / "laptops.xlsx"
__CONF = __PATH / "config.txt"


def download_laptop_info_to_json(price_range: str) -> None:
    dictlist = czc.laptop_links_to_dicts(czc.get_all_laptop_links(price_range))
    with open(__LAPTOPS_JSON, "w", encoding="utf-8") as file:
        json.dump(dictlist, file, ensure_ascii=False, indent=4)


def add_cpu_scores_to_json() -> None:
    if not __LAPTOPS_JSON.is_file():
        print(f"Soubor '{__LAPTOPS_JSON}' neexistuje. Začněte krokem 1.")
        return
    with open(__LAPTOPS_JSON, "r", encoding="utf-8") as file:
        dictlist = json.load(file)
    cpu.add_cpu_scores(dictlist)
    with open(__LAPTOPS_JSON, "w", encoding="utf-8") as file:
        json.dump(dictlist, file, ensure_ascii=False, indent=4)


def json_to_excel(biased: bool = False, print_progress: bool = True) -> None:
    if not __LAPTOPS_JSON.is_file():
        print(f"Soubor '{__LAPTOPS_JSON}' neexistuje. Začněte krokem 1.")
        return
    with open(__LAPTOPS_JSON, "r", encoding="utf-8") as file:
        dictlist = json.load(file)
    workbook = xlsxwriter.Workbook(__LAPTOPS_XCEL)
    worksheet = workbook.add_worksheet()
    is_first_iter = True
    row_n = 1
    for laptop_dict in dictlist:

        if (biased and (
                "lenovo" in laptop_dict["link"]
                or laptop_dict["Numerická klávesnice:"] != "Ano"
                or laptop_dict["Operační systém:"] == "Bez operačního systému"
        )):
            continue

        col_n = 0
        for key, value in laptop_dict.items():
            if is_first_iter:
                worksheet.write(0, col_n, key)
            worksheet.write(row_n, col_n, value)
            col_n += 1
        row_n += 1
        if print_progress:
            print(end="*", flush=True)
    workbook.close()


def price_range_save_to_txt(text: str) -> None:
    with open(__CONF, "w", encoding="utf-8") as file:
        file.write(text)


def price_range_read_from_txt() -> Optional[str]:
    if __CONF.is_file():
        with open(__CONF, "r", encoding="utf-8") as file:
            text = file.read()
            if ip.check_price_range(text):
                return text
    return None
