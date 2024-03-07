import json
import pathlib

import xlsxwriter

import cpubenchmark_scraper as cpu
import czc_laptop_scraper as czc

PATH = pathlib.Path(__file__).parent
LAPTOPS_JSON = PATH / "laptops.json"
LAPTOPS_XCEL = PATH / "laptops.xlsx"


def download_laptop_info_to_json() -> None:
    dictlist = czc.laptop_links_to_dicts(czc.get_all_laptop_links())
    with open(LAPTOPS_JSON, "w", encoding="utf-8") as file:
        json.dump(dictlist, file, ensure_ascii=False, indent=4)


def add_cpu_scores_to_json() -> None:
    if not LAPTOPS_JSON.is_file():
        print(f"Soubor '{LAPTOPS_JSON}' neexistuje. Začněte krokem 1.")
        return
    with open(LAPTOPS_JSON, "r", encoding="utf-8") as file:
        dictlist = json.load(file)
    cpu.add_cpu_scores(dictlist)
    with open(LAPTOPS_JSON, "w", encoding="utf-8") as file:
        json.dump(dictlist, file, ensure_ascii=False, indent=4)


def json_to_excel(print_progress: bool = True) -> None:
    if not LAPTOPS_JSON.is_file():
        print(f"Soubor '{LAPTOPS_JSON}' neexistuje. Začněte krokem 1.")
        return
    with open(LAPTOPS_JSON, "r", encoding="utf-8") as file:
        dictlist = json.load(file)
    workbook = xlsxwriter.Workbook(LAPTOPS_XCEL)
    worksheet = workbook.add_worksheet()
    is_first_iter = True
    row_n = 1
    for laptop_dict in dictlist:
        col_n = 0
        for key, value in laptop_dict.items():
            if is_first_iter:
                worksheet.write(0, col_n, key)
            worksheet.write(row_n, col_n, value)
            col_n += 1
        row_n += 1
        if print_progress:
            print(end="*")
    workbook.close()
