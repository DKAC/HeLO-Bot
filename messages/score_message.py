import datetime
from discord.embeds import Embed
from database_models import Clan, Clans, Match
from object_models import NewMatch
from object_state import not_empty
from user_state import UserState
from env import *
from data import *

class ScoresMessage:
    
    async def send(state:UserState):        
        clans = Clans.get()
        clans.sort(key = lambda clan: clan.score, reverse = True)

        description = "```asciidoc\n[ rank score clan ]\n" 
        i = 0
        for clan in clans:
            i += 1
            description += f"  {str(i).rjust(3)}  {str(clan.score).rjust(4)}  {clan.tag}\n"
            
        description += "```"
        
        embed = Embed(title=f"HeLO Ranking and Scores", description=description)
        embed.set_footer(text=f"{datetime.datetime.now().isoformat(sep=' ', timespec='minutes')}")
        channel = discordClient.get_channel(int(scores_channel))

        
        m = await channel.send(embed=embed)
        logging.info(f"added message: {m.id}")        
