import random

from ReferentielInsultes import insultes_sale, insultes_con_comme, insultes_prefix


def get_insulte_sale() -> str:
    return random.choice(insultes_sale)


def get_insulte_con_comme() -> str:
    return random.choice(insultes_con_comme)


def get_insulte_generique(sale=True, con=False) -> str:
    insulte = ""

    if sale:
        insulte += f"{random.choice(insultes_prefix)} {get_insulte_sale()}"

    if con:
        if sale:
            insulte += ", "

        insulte += f"t'es {get_insulte_con_comme()} ou quoi ?"

    return insulte


def get_insultes(nombre=1) -> str:
    insultes = ""
    prefix_index = 0

    for i in range(nombre):
        insulte_type = random.randint(0, 10)

        if insulte_type < 2:
            # 20% t'es _ ou quoi ?
            insultes += f"t'es {get_insulte_con_comme()} ou quoi ?"

            if i + 1 < nombre:
                insultes += " "
        else:
            # 80% insulte générique
            insultes += f"{insultes_prefix[prefix_index]} {get_insulte_sale()}"

            # On fait avancer l'index des prefix pour éviter les répétitions
            prefix_index += 1
            if prefix_index >= len(insultes_prefix):
                prefix_index = 0

            if i + 1 < nombre:
                insultes += ", "

    return insultes
