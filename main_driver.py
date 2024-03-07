import file_io as f


def __print_menu() -> None:
    print("\n===\n"
          "1 - Stáhnout informace o noteboocích z czc do laptops.json\n"
          "2 - Přidat CPU skóre z cpubenchmark do laptops.json\n"
          "3 - Vytvořit Excel tabulku: laptops.json -> laptops.xlsx\n"
          "0 - Exit")


def __main() -> None:
    print("CZC Laptop Chooser v0.0")
    while True:
        __print_menu()
        match input(">>> "):
            case "0":
                return

            case "1":
                f.download_laptop_info_to_json()

            case "2":
                f.add_cpu_scores_to_json()

            case "3":
                f.json_to_excel()

            case _:
                print("Neznámý příkaz")


if __name__ == "__main__":
    __main()
