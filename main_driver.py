import json
import pathlib

import cpubenchmark_scraper as cpu
import czc_laptop_scraper as czc

PATH = pathlib.Path(__file__).parent
LAPTOPS_JSON = PATH / "laptops.json"


def __print_menu() -> None:
    print("\n===\n"
          "1 - Stáhnout informace o noteboocích z czc do laptops.json\n"
          "2 - Přidat CPU skóre z cpubenchmark do laptops.json\n"
          "3 - Vytvořit Excel tabulku: laptops.json -> laptops.xlsx\n"
          "0 - Exit")


def __main() -> None:
    print("CZC Laptop Chooser v-1.1")
    while True:
        __print_menu()
        match input(">>> "):
            case "0":
                return

            case "1":
                dictlist = czc.laptop_links_to_dicts(czc.get_all_laptop_links())
                with open("laptops.json", "w", encoding="utf-8") as file:
                    json.dump(dictlist, file, ensure_ascii=False, indent=4)

            case "2":
                if not LAPTOPS_JSON.is_file():
                    print(f"Soubor '{LAPTOPS_JSON}' neexistuje. Začněte krokem 1.")
                    continue
                with open("data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                cpu.get_all_cpu_scores(data)


if __name__ == "__main__":
    __main()
