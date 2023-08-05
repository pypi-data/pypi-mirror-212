def get_description(age: int) -> str:
    if age < 14:
        return "Dziecko"
    if age < 18:
        return "Nastolatek"
    if age < 30:
        return "Młody"
    if age < 50:
        return "Dojrzały"
    if age < 65:
        return "Wiekowy"
    return "Emeryt"
