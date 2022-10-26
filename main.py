# bot.py
import os
import validators

import discord

from discord.ext.commands import Bot
from dotenv import load_dotenv
from validators import ValidationFailure

from BanList import BanList

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CSV_FILE = os.getenv('CSV_FILE')

banlist = BanList(CSV_FILE)

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    bot.tree.copy_global_to(guild=guild)

    await bot.tree.sync(guild=guild)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.hybrid_command()
async def menu(ctx):
    view = Menu()
    await ctx.reply(view=view)


class Menu(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="TESTE TON DECK RACAILLE 🤖🔍", style=discord.ButtonStyle.primary)
    async def menu_decktest(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalTestDeck())

    @discord.ui.button(label="❌BANLIST❌", style=discord.ButtonStyle.grey)
    async def menu_banlist(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = f"--❌❌BANLIST❌❌--\n"

        message += banlist.get_banlist()

        discord.Embed(description=message)

        await interaction.response.edit_message(content=message, view=None)

    @discord.ui.button(label="BAN UNE CARTE 🎴➡🗑️", style=discord.ButtonStyle.red)
    async def menu_bancard(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalBanCarte())

    @discord.ui.button(label="UNBAN UNE CARTE 🎴➡✔️", style=discord.ButtonStyle.green)
    async def menu_unbancard(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


class ModalTestDeck(discord.ui.Modal, title="Rentre ta decklist"):

    decklist = discord.ui.TextInput(label="Decklist", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Decklist", description=f"{self.decklist}")
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

        await interaction.response.edit_message(embed=embed, view=None)


class ModalBanCarte(discord.ui.Modal, title="Ban ta carte"):

    carte = discord.ui.TextInput(label="Nom", style=discord.TextStyle.short, required=True)
    raison = discord.ui.TextInput(label="Raison du ban", style=discord.TextStyle.long, required=False, max_length=100)
    link = discord.ui.TextInput(label="Lien vers la carte", style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        message = f"--{interaction.user.mention} A BANNI LA CARTE **{self.carte}** 🗑️🗑️--"
        embed = None

        if str(self.raison):
            embed = discord.Embed(description=f"{self.raison}")
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)

        card_link = ""
        if str(self.link):
            try:
                validators.url(str(self.link))
                card_link = self.link
            except ValidationFailure:
                pass

        if banlist.add_ban(str(self.carte), str(interaction.user.name), str(self.raison), card_link) == 0:
            await interaction.response.edit_message(content=message, embed=embed, view=None)
        else:
            await interaction.response.edit_message(content=f"--**{self.carte}** EST DEJA BANNIE BOUFFON--", view=None)


bot.run(TOKEN)
