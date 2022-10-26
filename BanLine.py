
class BanLine:

    def __init__(self, carte: str, auteur: str, raison: str = "", lien: str = ""):
        self.carte = carte
        self.raison = raison
        self.lien = lien
        self.auteur = auteur

    def get_csv_row(self) -> list[any]:
        return [self.carte, self.auteur, self.raison, self.lien]

    def __eq__(self, other):
        return self.carte == other.carte

    def __str__(self):
        if self.lien:
            return f"[{self.carte}]({self.lien})"
        else:
            return self.carte
