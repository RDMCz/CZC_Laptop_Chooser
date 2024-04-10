from typing import Optional


def user_input_price_range() -> Optional[str]:
    user_input = input("Zadejte min a max ceny oddělené spojovníkem (např. 9900-16000):")
    if check_price_range(user_input):
        return user_input
    return None


def check_price_range(text: str) -> bool:
    parts = text.split("-")
    if len(parts) == 2:
        min_price_stripped = parts[0].strip()
        max_price_stripped = parts[1].strip()
        if min_price_stripped.isdecimal() and max_price_stripped.isdecimal():
            min_price_int = int(parts[0])
            max_price_int = int(parts[1])
            if max_price_int >= min_price_int:
                return True
    return False
