from typing import Optional
import nextcord
import datetime
from nextcord.ext import commands
from helpers import jsonHelper, embedHelper
config = jsonHelper.loadConfig()
guilds = [1195843192428433468]

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
    hours = sheet.col_values(5, value_render_option='FORMULA')
    amount = sheet.col_values(2, value_render_option='FORMULA')
    for ind in range(len(data)):
        data[ind][7] = formulas[ind]
        data[ind][4] = hours[ind]
        data[ind][1] = amount[ind]
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
        
    sheet = tables.worksheet("Updates")
    sheet.update('A1', data, raw = False)
    sheet.update('L1', reasons, raw = False)

def updateCsv(data):
    with open("data/money.csv", 'w+', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerows(data)

def create_itemview(list):
    items = []
    for item in list:
        date = [int(x) for x in item[0].split("/")]
        date = datetime.datetime(date[2], date[0], date[1]).timestamp()
        items.append([
            item[8], # Reason
            int(item[9]), # Index
            date, # Date
            float(item[1][1:].replace(',', '')), # Impact
            item[2], # Source
            item[5], # Paid?
            item[6], # Deposit?
        ])
    
    itemview = ItemView()
    itemview.fullData = items
    return itemview

class ItemView(nextcord.ui.View):
    sortType = 1
    curr_page = 0
    items_per_page = 4
    def __init__(self):
        super().__init__(timeout = 30)
        self.value = None

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        self.first_button.disabled = True
        self.back_button.disabled = True
        self.last_button.disabled = True
        self.next_button.disabled = True
        self.sort_button.disabled = True
        self.reverse_button.disabled = True
        await self.message.edit(embed=embedHelper.defaultEmbed(
            "Select a View",
            ""
        ), view=self)
        # await self.update_message()

    def sort(self):
        self.data.sort(key = lambda x: x[self.sortType])

    def advanceSort(self):
        self.sortType = (self.sortType + 1) % 4

    def create_embed(self, items):
        formatted = []
        for item in items:
            if(item[6] == 'FALSE'):
                item[3] *= -1

            formatted.append([
                item[0],
                f"Index: `{item[1]}`\n" +
                f"Date: `{datetime.datetime.fromtimestamp(item[2]).strftime('%m/%d/%Y')}`\n" +
                f"Impact: `${'{0:.2f}'.format(item[3])}`\n" +
                f"Source: `{item[4]}`\n" + 
                f"Paid?: `{item[5]}`\n"
            ])
        if(self.sortType == 0):
            sortMess = "Name"
        elif(self.sortType == 1):
            sortMess = "Index"
        elif(self.sortType == 2):
            sortMess = "Date"
        elif(self.sortType == 3):
            sortMess = "Impact"
        formatted.append(["", f"Page Number: {self.curr_page + 1}"])
        return embedHelper.listEmbed("Unpaid Items", "Sorting by: " + sortMess, formatted)
    
    def update_buttons(self):
        self.sort_button.disabled = False
        self.reverse_button.disabled = False
        if(self.curr_page == 0):
            self.first_button.disabled = True
            self.back_button.disabled = True
            self.first_button.style = nextcord.ButtonStyle.gray
            self.back_button.style = nextcord.ButtonStyle.gray
        else:
            self.first_button.disabled = False
            self.back_button.disabled = False
            self.first_button.style = nextcord.ButtonStyle.blurple
            self.back_button.style = nextcord.ButtonStyle.blurple

        if(self.curr_page == (len(self.data)-1) // self.items_per_page):
            self.last_button.disabled = True
            self.next_button.disabled = True
            self.last_button.style = nextcord.ButtonStyle.gray
            self.next_button.style = nextcord.ButtonStyle.gray
        else:
            self.last_button.disabled = False
            self.next_button.disabled = False
            self.last_button.style = nextcord.ButtonStyle.blurple
            self.next_button.style = nextcord.ButtonStyle.blurple

    async def update_message(self):
        self.update_buttons()
        items = self.data[self.curr_page * self.items_per_page:(self.curr_page + 1) * self.items_per_page]
        await self.message.edit(embed=self.create_embed(items), view=self)

    @nextcord.ui.string_select(
        placeholder="What would you like to view?",
        options=[
            nextcord.SelectOption(label="All", value="0", description="List all entries in the database."),
            nextcord.SelectOption(label="Unpaid", value="1", description="List all unpaid entries in the database."),
            nextcord.SelectOption(label="Deposits", value="2", description="List all deposit entries in the database."),
            nextcord.SelectOption(label="Payments", value="3", description="List all spending entries in the database."),
        ]
    )
    async def select(self, select: nextcord.ui.StringSelect, ctx: nextcord.Interaction):
        tempData = []
        if(select.values[0] == "0"):
            tempData = self.fullData

        if(select.values[0] == "1"):
            for item in self.fullData:
                if(item[5] == 'FALSE'):
                    tempData.append(item)

        if(select.values[0] == "2"):
            for item in self.fullData:
                if(item[6] == 'TRUE'):
                    tempData.append(item)

        if(select.values[0] == "3"):
            for item in self.fullData:
                if(item[6] == 'FALSE'):
                    tempData.append(item)

        self.data = tempData
        self.curr_page = 0
        self.sort()
        await self.update_message()

    @nextcord.ui.button(label = "|<", style=nextcord.ButtonStyle.blurple)
    async def first_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.curr_page = 0
        await self.update_message()
    
    @nextcord.ui.button(label = "<", style=nextcord.ButtonStyle.blurple)
    async def back_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.curr_page -= 1
        await self.update_message()
    
    @nextcord.ui.button(label = ">", style=nextcord.ButtonStyle.blurple)
    async def next_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.curr_page +=1
        await self.update_message()
    
    @nextcord.ui.button(label = ">|", style=nextcord.ButtonStyle.blurple)
    async def last_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.curr_page = (len(self.data) -1) // self.items_per_page
        await self.update_message()
    
    @nextcord.ui.button(label = "", style=nextcord.ButtonStyle.success, emoji="\U0001F504")
    async def sort_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.advanceSort()
        self.sort()
        self.curr_page = 0
        await self.update_message()
    
    @nextcord.ui.button(label = "", style=nextcord.ButtonStyle.success, emoji="\U00002195")
    async def reverse_button(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        await ctx.response.defer()
        self.data.reverse()
        await self.update_message()

    async def on_timeout(self):
        self.first_button.disabled = True
        self.back_button.disabled = True
        self.last_button.disabled = True
        self.next_button.disabled = True
        self.sort_button.disabled = True
        self.reverse_button.disabled = True
        self.select.disabled = True

        await self.message.edit(embed=embedHelper.defaultEmbed(
            "This View Has Expired",
            "Too much time has elapsed since this window was interacted with."
        ), view=self)

async def send_data(bot, ctx: Optional[int] = None):
    sheet = tables.worksheet("Data")
    if(ctx == None):
        ctx = bot.get_channel(1196581541522980987)

    raw = sheet.get_all_values()

    data = []
    data.append(["Current Total", raw[3][1]])
    data.append(["Current Savings", raw[0][4]])
    data.append(["Current Excess", raw[0][7]])

    await ctx.send(embed=embedHelper.listEmbed(
        "Savings Statistics",
        f"{datetime.datetime.today().strftime('%B %d, %Y')}\n" + 
        f"{datetime.datetime.today().strftime('%I:%M:%S %p')}",
        data
    ))

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def stats(self, ctx):
        await send_data(self.bot, ctx)

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def money(self, ctx):
        """
        Commands pertaining to the money tracking database.
        """
        pass

    @money.subcommand()
    async def entry(self, ctx):
        """
        Commands pertaining to a given entry in the tracking database.
        """
        pass
    
    @entry.subcommand()
    async def change(self, ctx, 
            index: int = nextcord.SlashOption(description="Index of entry to be viewed."),
            section: str = nextcord.SlashOption(description="Section to be modified", choices={
                "Date":"0",
                "Amount":"1",
                "Dollars/Hr":"3",
                "Paid?":"5",
                "Deposit?":'6',
                "Excess %":"7",
                }),
            newval: str = nextcord.SlashOption(description="New value to be input.")
        ):
        """
        Update a given entries information given a section and new data.
        """
        data = dataFromCsv()
        
        data[index][int(section)] = newval

        updateSheet(data)
        updateCsv(dataFromSheet())

        await ctx.send(embed = embedHelper.defaultEmbed(
            "Change Successful!",
            "Updated data pushed to the database successfully."
        ))
        await send_data(self.bot)

    @entry.subcommand()
    async def show(self, ctx, 
            index: int = nextcord.SlashOption(description="Index of entry to be viewed.")
        ):
        """
        Display a given entries information given the index.
        """
        data = dataFromCsv()
        item = data[index]

        await ctx.send(embed = embedHelper.defaultEmbed(
            item[-1],
            f"Index: `{index}`\n" + 
            f"Date: `{item[0]}`\n" + 
            f"Amount: `{item[1]}`\n" +
            f"Type: `{item[2]}`\n" + 
            f"$/Hr: `{item[3]}`\n" +
            f"Paid?: `{item[5]}`\n" +
            f"Deposit?: `{item[6]}`\n" +
            f"Excess %: `{item[7]}`\n"
        ))

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
        await send_data(self.bot)

    @money.subcommand()
    async def spend(self, ctx, 
                    spent: float = nextcord.SlashOption(description="How much was spent?"),
                    personal: str = nextcord.SlashOption(description="Was the purchase personal?", choices={"Yes":"Spending (P)", "No":"Spending (S)", "Food":"Food"}),
                    reason:str = nextcord.SlashOption(description="What was the purchase for?")
                    ):
        """
        Add a purchase made to the database.
        """
        data = dataFromCsv()

        if(personal == 'Spending (P)'):
            excess = '=1'
        elif(personal == 'Spending (S)'):
            excess = '=0'
        else:
            excess = '=1/2'
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
        await send_data(self.bot)

    @money.subcommand()
    async def prespend(self, ctx, 
                    spent: float = nextcord.SlashOption(description="How much was spent?"),
                    personal: str = nextcord.SlashOption(description="Was the purchase personal?", choices={"Yes":"Spending (P)", "No":"Spending (S)", "Food":"Food"}),
                    reason:str = nextcord.SlashOption(description="What was the purchase for?")
                    ):
        """
        Add a future purchase made to the database.
        """
        data = dataFromCsv()

        if(personal == 'Spending (P)'):
            excess = '=1'
        elif(personal == 'Spending (S)'):
            excess = '=0'
        else:
            excess = '=1/2'
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
        await send_data(self.bot)

    @money.subcommand()
    async def deposit(self, ctx,
                    date: str = nextcord.SlashOption(description="What date will this be recieved? (M/D/Y)"),
                    deposited: float = nextcord.SlashOption(description="How much are you depositing?"),
                    work: str = nextcord.SlashOption(description="Is this deposit from work?", choices={"Yes":"Work", "No":"Other"}),
                    recieved: str = nextcord.SlashOption(description="Has this been recieved yet?", choices={"Yes":'TRUE', "No":'FALSE'}),
                    reason: str = nextcord.SlashOption(description="Where is the deposit from?", required=False),
                    ):
        """
        Add a purchase made to the database.
        """
        data = dataFromCsv()

        if(work == "Work"):
            reason = "ITS Work (Trainee)"
        
        data.append([
            date,
            f'${deposited}',
            work,
            '','',
            recieved, 'TRUE',
            '=1/3',
            reason
        ])

        updateSheet(data)
        updateCsv(dataFromSheet())

        await ctx.send(embed = embedHelper.sucEmbed(
            "Update Successful!",
            "Added deposit to the database."
        ))
        await send_data(self.bot)

    @money.subcommand()
    async def list(self, ctx):
        """
        List items that haven't been paid for.
        This could be a future wage, debt, or planned purchase.
        """
        data = dataFromCsv()[1:]
        for ind in range(len(data)):
            data[ind].append(ind)

        unpaid_view = create_itemview(data)
        await unpaid_view.send(ctx)

def setup(bot):
  bot.add_cog(Money(bot))