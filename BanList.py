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
