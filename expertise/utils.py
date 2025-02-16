from num2words import num2words  # ✅ Import de num2words

def nombre_en_lettres(nombre):
    """
    Convertit un nombre en toutes lettres en français.
    """
    return num2words(nombre, lang='fr').capitalize()