import file_io as f
import input_parser as ip


class CZCLaptopChooser:
    __DEFAULT_PRICE_RANGE = "10000-20000"

    def __init__(self):
        temp = f.price_range_read_from_txt()
        self.__price_range = temp if temp else self.__DEFAULT_PRICE_RANGE

    def __print_menu(self) -> None:
        print(f"\n===\nHledání notebooků v cenovém rozsahu {self.__price_range} Kč\n"
              "1 - Stáhnout informace o noteboocích z czc do laptops.json\n"
              "2 - Přidat CPU skóre z cpubenchmark do laptops.json\n"
              "3 - Vytvořit Excel tabulku: laptops.json -> laptops.xlsx\n"
              "9 - Změnit cenový rozsah\n"
              "0 - Exit")

    def main(self) -> None:
        print("CZC Laptop Chooser v0.1")
        while True:
            self.__print_menu()
            match input(">>> "):
                case "0":
                    return

                case "1":
                    f.download_laptop_info_to_json(self.__price_range)

                case "2":
                    f.add_cpu_scores_to_json()

                case "3":
                    f.json_to_excel()

                case "3B":
                    f.json_to_excel(True, True)

                case "9":
                    user_input = ip.user_input_price_range()
                    if user_input:
                        self.__price_range = user_input
                        f.price_range_save_to_txt(user_input)
                    else:
                        print("Špatně zadaný cenový rozsah")

                case _:
                    print("Neznámý příkaz")


if __name__ == "__main__":
    program = CZCLaptopChooser()
    program.main()
