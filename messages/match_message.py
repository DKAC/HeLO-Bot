import datetime
from discord.embeds import Embed
from database_models import Clan, Clans, Match
from object_models import NewMatch
from object_state import not_empty
from user_state import UserState
from env import *

class MatchMessage:
    
    async def send(state:UserState):        
        embed = Embed(title=match_title(state), description=match_description(state))
        embed.set_footer(text=get_match(state).match_id)
        channel = discordClient.get_channel(int(matches_channel))

        # todo do we need changes more than 14 days ago?
        
        after_date = datetime.datetime.utcnow()-datetime.timedelta(days=14)
        messages = await channel.history(after=after_date).flatten()
        match = get_match(state)
        if match != None:
            for m in messages:
                if len(m.embeds) > 0:
                    if m.embeds[0].footer != None:                    
                        if m.embeds[0].footer.text == get_match(state).match_id:
                            await m.edit(embed=embed)                            
                            logging.info(f"edit message: {m.id}")
                            return
        
        await channel.send(embed=embed)


def get_match(state):
    new_match = state.find(NewMatch)    
    return new_match.match if new_match != None else None
            
        
def match_title(state):
    match = get_match(state)
    if match == None: return ""
    
    title = f"{match.date} {match.clan1}"
    if not_empty(match.coop1): title += f" {match.coop1}"
    title += f" vs. {match.clan2}"
    if not_empty(match.coop1): title += f" {match.coop2}"
    return title


def match_description(state):
    match = get_match(state)
    if match == None: return ""
    
    clans = Clans.get()
    
    # todo store id instead of tag
    dummy = Clan("dummy", tag = "???")
    clan1 = [clan for clan in clans if clan.id == match.clan1_id][0] if match.clan1 != None and match.clan1 != "" else dummy
    coop1 = [clan for clan in clans if clan.id == match.coop1_id][0] if match.coop1 != None and match.coop1 != "" else dummy
    clan2 = [clan for clan in clans if clan.id == match.clan2_id][0] if match.clan2 != None and match.clan2 != "" else dummy
    coop2 = [clan for clan in clans if clan.id == match.coop2_id][0] if match.coop2 != None and match.coop2 != "" else dummy
    
    s = ""
    s += f"{clan1.flag} "   if not_empty(clan1.flag)  else ""
    s += f"{clan1.tag}"
    s += " & "              if not_empty(match.coop1) else ""
    s += f"{coop1.flag} "   if not_empty(coop1.flag)  else ""
    s += f"{coop1.tag}"     if not_empty(match.coop1) else ""
    s += " vs. "
    s += f"{clan2.flag} "   if not_empty(clan2.flag)  else ""
    s += f"{clan2.tag}"
    s += " & "              if not_empty(match.coop2) else ""
    s += f"{coop2.flag} "   if not_empty(coop2.flag)  else ""
    s += f"{coop2.tag}"     if not_empty(match.coop2) else ""
    s += "\n"
    s += f":calendar_spiral: {match.date}" if match.date != None else "???"
    s += "\n"
    s += f":map: {match.map}" if not_empty(match.map) else "???"
    s += "\n"
    s += emoji_side[match.side1] if not_empty(match.side1) else "???"
    s += "  "
    s += emoji_number[match.caps1] if match.caps1 != None else "?"
    s += " : "
    s += emoji_number[match.caps2] if match.caps2 != None else "?"
    s += "  "
    s += emoji_side[match.side2] if not_empty(match.side2) else "???"
    s += "\n\n"
    return s    


def match_footer(state):
    match = get_match(state)
    if match == None: return ""
    
    return match.match_id
