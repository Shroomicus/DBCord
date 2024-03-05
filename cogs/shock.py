import requests
import threading
import random

import nextcord
import datetime
from nextcord.ext import commands
from helpers import jsonHelper, embedHelper
config = jsonHelper.loadConfig()
guilds = config["guilds"]

url = 'https://do.pishock.com/Client/LinkOperate'

modes = {
    "shock" : 's',
    "vibrate" : 'v',
    'beep' : 'b'
}

# actually the other button sends duration 300?
def shock(int, dur, mode):
    body = {
        "Intensity":int,
        "Duration":dur,
        "Id":"4bff9764-c1ed-4212-94dd-31acfc80a175",
        "Key":"06731dcd-54c3-4d3f-834a-db661c6076aa",
        "Op":mode,
        "Hold":False,
        "Username":"Discord Bot :3"
    }

    x = requests.post(url, json = body)
    return x.text


class Shock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def shock(self, ctx,
            power: int = nextcord.SlashOption(description="Shock strength (between 1-5)"),
        ):
        """
        Shock a dog!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (1 <= power <= 5)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Please input a value between 1 and 5 for shock strength."
            ))
            return
        if(shock(power, 100, 's') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Shock Successful!",
            "Please await your whines."
        ))

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def multishock(self, ctx,
            power: int = nextcord.SlashOption(description="Shock strength (between 1-5)"),
            times: int = nextcord.SlashOption(description="How many times to shock (between 1-25)")
        ):
        """
        Shock a really BAD dog!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (1 <= power <= 5)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Please input a value between 1 and 5 for shock strength."
            ))
            return
        if(not (1 <= times <= 25)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Please input a value between 1 and 25 for times to shock."
            ))
            return
        if(shock(power, 100, 's') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Shock Successful!",
            "Please await your whines."
        ))
        for i in range(times-1):
            x = power
            shock(x, 100, modes["shock"])
    
    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def beep(self, ctx,
        ):
        """
        Beep beep!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(shock(1, 100, 'b') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Beep Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Beep Successful!",
            "Please await your whines."
        ))

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def multibeep(self, ctx,
            times: int = nextcord.SlashOption(description="How many times to beep (between 1-25)")
        ):
        """
        BEEP BEEP BEEP BEEP BEEP BEEP BEEP BEEP BEEP
        """
        whitelist = jsonHelper.getJson("whitelist.json")
        if(id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (1 <= times <= 25)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Beep Unsuccessful!",
                "Please input a value between 1 and 25 for times to Beep."
            ))
            return
        if(shock(1, 100, 'b') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Beep Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Beep Successful!",
            "Please await your beeps."
        ))
        for i in range(times-1):
            shock(1, 100, modes["beep"])
    
    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def vibe(self, ctx,
            power: int = nextcord.SlashOption(description="Vibration strength (between 1-40)"),
        ):
        """
        Vibe a dog!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (1 <= power <= 40)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibe Unsuccessful!",
                "Please input a value between 1 and 5 for vibration strength."
            ))
            return
        if(shock(power, 100, 'v') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibe Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Vibe Successful!",
            "Please await your whines."
        ))

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def multivibe(self, ctx,
            power: int = nextcord.SlashOption(description="Vibe strength (between 1-40)"),
            times: int = nextcord.SlashOption(description="How many times to vibrate (between 1-25)")
        ):
        """
        Vibe a really GOOD dog!
        """
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(ctx.user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Shock Unsuccessful!",
                "You are not whitelisted!"
            ))
            return
        if(not (1 <= power <= 40)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibe Unsuccessful!",
                "Please input a value between 1 and 5 for vibe strength."
            ))
            return
        if(not (1 <= times <= 25)):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibe Unsuccessful!",
                "Please input a value between 1 and 25 for times to vibe."
            ))
            return
        if(shock(power, 100, 'v') == "Shocker is Paused or does not exist. Unpause to send command."):
            await ctx.send(embed = embedHelper.errEmbed(
                "Vibe Unsuccessful!",
                "Shocker is paused! Booooo!!!!!!"
            ))
            return
        await ctx.send(embed = embedHelper.sucEmbed(
            "Vibe Successful!",
            "Please await your whines."
        ))
        for i in range(times-1):
            x = power
            shock(x, 100, modes["vibrate"])
        
    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def whitelist(self, ctx,
            user: nextcord.Member = nextcord.SlashOption(description="User to whitelist")
        ):
        """
        Whitelist a user!
        """
        if(ctx.user.id != 481111824734093322):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"You aren't slaughtumn."
            ))
            return
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(user.id in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"User already whitelisted."
            ))
            return
        whitelist.append(user.id)
        jsonHelper.setJson("data/whitelist.json", whitelist)
        
        await ctx.send(embed = embedHelper.sucEmbed(
            "Whitelist Successful!",
            f"Whitelisted <@{user.id}>"
        ))

    @nextcord.slash_command(
        guild_ids=guilds
    )
    async def unwhitelist(self, ctx,
            user: nextcord.Member = nextcord.SlashOption(description="User to unwhitelist")
        ):
        """
        Unwhitelist a user!
        """
        if(ctx.user.id != 481111824734093322):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"You aren't slaughtumn."
            ))
            return
        whitelist = jsonHelper.getJson("data/whitelist.json")
        if(user.id not in whitelist):
            await ctx.send(embed = embedHelper.errEmbed(
                "Whitelist Failed!",
                f"User not whitelisted."
            ))
            return
        whitelist.remove(user.id)
    
        jsonHelper.setJson("data/whitelist.json", whitelist)
        
        await ctx.send(embed = embedHelper.sucEmbed(
            "Unwhitelist Successful!",
            f"Unwhitelisted <@{user.id}>"
        ))

def setup(bot):
  bot.add_cog(Shock(bot))