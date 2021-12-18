import logging, os, pytz, discord
from discord_components.client import DiscordComponents

discord_token = os.environ.get("DISCORD_TOKEN")
matches_channel = os.environ.get("MATCHES_CHANNEL")
heloUrl = os.environ.get("HELO_URL")

tz = pytz.timezone("Europe/Berlin")

logging.basicConfig(encoding='utf-8', level=logging.INFO, format=f"%(filename)20s:%(lineno)-3s - %(funcName)-30s %(message)s")
logging.getLogger("discord").setLevel(logging.ERROR)

discordClient = discord.Client()
DiscordComponents(discordClient)

emoji_side = { "Allies": "<:Allies:921762173590581299>", "Axis": "<:Axis:921762520899924050>" }
emoji_number = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:"]
