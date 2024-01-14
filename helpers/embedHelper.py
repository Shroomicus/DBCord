from datetime import datetime
import nextcord

def defaultEmbed(title, description):
  defaultColor = nextcord.Colour.from_rgb(255,53,53)
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = defaultColor,
    #timestamp=datetime.now()
  )
  # embed.set_author(
  #   name = "redlink", 
  #   icon_url = "https://cdn.discordapp.com/avatars/1068987178882961508/6f3711da54540d09e76668dd30bcfacf.webp?size=300"
  # )
  # embed.set_footer(text="redlink")
  return embed

def logEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.light_gray(),
    timestamp=datetime.now()
  )
  # embed.set_author(
  #   name = "redlink", 
  #   icon_url = "https://cdn.discordapp.com/avatars/1068987178882961508/6f3711da54540d09e76668dd30bcfacf.webp?size=300"
  # )
  # embed.set_footer(text="redlink")
  return embed

def errEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.red(),
    timestamp=datetime.now()
  )
  # embed.set_author(
  #   name = "redlink", 
  #   icon_url = "https://cdn.discordapp.com/avatars/1068987178882961508/6f3711da54540d09e76668dd30bcfacf.webp?size=300"
  # )
  # embed.set_footer(text="redlink")
  return embed

def sucEmbed(title, description):
  embed = nextcord.Embed(
    title = title,
    description = description,
    color = nextcord.Colour.green(),
    timestamp=datetime.now()
  )
  # embed.set_author(
  #   name = "redlink", 
  #   icon_url = "https://cdn.discordapp.com/avatars/1068987178882961508/6f3711da54540d09e76668dd30bcfacf.webp?size=300"
  # )
  # embed.set_footer(text="redlink")
  return embed