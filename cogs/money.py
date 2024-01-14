import nextcord
import datetime
from nextcord.ext import commands
from helpers import jsonHelper, embedHelper
config = jsonHelper.loadConfig()
guilds = config["guilds"]

import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'gkey.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

tables = client.open_by_key('1-EEmcUjINw-mqsp76bYiYPJwkYngOa1MeQ1KWTUO6Xk')

def dataFromSheet():
    sheet = tables.worksheet("Updates")
    data = sheet.get_all_values()
    data = [item for item in data if item[0] != '']
    formulas = sheet.col_values(8, value_render_option='FORMULA')
    for ind in range(len(data)):
        data[ind][7] = formulas[ind]
        temp = data[ind][-1]
        data[ind] = data[ind][:8]
        data[ind].append(temp)
    return data

def dataFromCsv():
    updateCsv(dataFromSheet())
    data = []
    with open("data/money.csv", 'r') as file:
        csvreader = csv.reader(file)
        for item in csvreader:
            data.append(item)
    return data

def updateSheet(data):
    reasons = []
    for ind in range(len(data)):
        reasons.append([data[ind][-1]])
        data[ind] = data[ind][:len(data[ind])-1]

    # print(reasons)
        
    sheet = tables.worksheet("Updates")
    sheet.update('A1', data, raw=False)
    sheet.update('L1', reasons, raw = False)

def updateCsv(data):
    with open("data/money.csv", 'w+', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(data)

    
class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def money(self, ctx):
        """
        Commands pertaining to the money tracking database.
        """
        pass



    @money.subcommand()
    async def update(self, ctx):
        """
        Update bot's data with that from the google sheet
        """
        updateCsv(dataFromSheet())
        await ctx.send(embed = embedHelper.sucEmbed(
            "Update Successful!",
            "Internal payment data has been fully updated."
        ))

    @money.subcommand()
    async def spend(self, ctx, 
                    spent: float = nextcord.SlashOption(description="How much was spent?"),
                    personal: str = nextcord.SlashOption(description="Was the purchase personal?", choices={"Yes":"Spending (P)", "No":"Spending (S)"}),
                    reason:str = nextcord.SlashOption(description="What was the purchase for?")
                    ):
        """
        Add a purchase made to the database.
        """
        data = dataFromCsv()

        if(personal == 'Spending (P)'):
            excess = '=1'
        else:
            excess = '=0'
        data.append([
            datetime.datetime.today().strftime('%m/%d/%Y'),
            f'${spent}',
            personal,
            '','',
            'TRUE', 'FALSE',
            excess,
            reason
        ])

        updateSheet(data)
        updateCsv(dataFromSheet())

        await ctx.send(embed = embedHelper.sucEmbed(
            "Update Successful!",
            "Added purchase to the database."
        ))

    @money.subcommand()
    async def prespend(self, ctx, 
                    spent: float = nextcord.SlashOption(description="How much was spent?"),
                    personal: str = nextcord.SlashOption(description="Was the purchase personal?", choices={"Yes":"Spending (P)", "No":"Spending (S)"}),
                    reason:str = nextcord.SlashOption(description="What was the purchase for?")
                    ):
        """
        Add a future purchase made to the database.
        """
        data = dataFromCsv()

        if(personal == 'Spending (P)'):
            excess = '=1'
        else:
            excess = '=0'
        data.append([
            datetime.datetime.today().strftime('%m/%d/%Y'),
            f'${spent}',
            personal,
            '','',
            'FALSE', 'FALSE',
            excess,
            reason
        ])

        updateSheet(data)
        updateCsv(dataFromSheet())

        await ctx.send(embed = embedHelper.sucEmbed(
            "Update Successful!",
            "Added purchase to the database."
        ))

    @money.subcommand()
    async def list_unpaid(self, ctx):
        """
        List items that haven't been paid for.
        This could be a future wage, debt, or planned purchase.
        """
        data = dataFromCsv()
        unpaid = []
        for ind in range(len(data)):
            if(data[ind][5] == "FALSE"):
                unpaid.append(data[ind])
                unpaid[-1].append(ind)
    
        print(unpaid)

        await ctx.send(embed = embedHelper.sucEmbed(
            "TESTING",
            "TESTING"
        ))

def setup(bot):
  bot.add_cog(Money(bot))