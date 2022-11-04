import csv
import os

from BanLine import BanLine


class BanList:

    def __init__(self, filename: str):
        self.filename = filename
        self.banlist: list[BanLine] = []
        self.read_bans_from_csv()

    def add_ban(self, carte: str, auteur: str, raison: str, lien: str):
        new_ban = BanLine(carte, auteur, raison, lien)
        if new_ban not in self.banlist:
            self.banlist.append(new_ban)
            self.write_bans_to_csv()
            return 0

        return -1

    def remove_ban(self, carte: str):
        self.banlist = list(filter(lambda l: l.carte.lower() != carte.lower(), self.banlist))

    def write_bans_to_csv(self):
        try:
            with open(self.filename, 'w+', newline='') as f:
                writer = csv.writer(f)
                for ban in self.banlist:
                    writer.writerow(ban.get_csv_row())
        except Exception as e:
            print(f"Exception lors de l'écriture de la banlist : {e}")

    def read_bans_from_csv(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.banlist.append(BanLine(row[0], row[1], row[2]))

    def get_banlist(self):
        message = "\n"
        for ban in self.banlist:
            message += f"**{ban}** banni par {ban.auteur} {': ' + ban.raison if ban.raison else ''}\n"

        return message

    def test_decklist(self, lines: list[str]) -> list[BanLine]:
        """
        Parcourt la liste de cartes renseignée pour déterminer si elle contient une ou plusieurs cartes bannies
        """

        invalid_cards: list[BanLine] = []

        for line in lines:
            for banned in self.banlist:
                if banned.carte.lower() in line.lower() and banned not in invalid_cards:
                    # Carte bannie
                    invalid_cards.append(banned)

        return invalid_cards
