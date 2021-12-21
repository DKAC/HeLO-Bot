from datetime import date, timedelta
import logging
from types import SimpleNamespace
from typing import List
import discord
from discord_components.component import Button
from database_models import Match, Matches
from object_models import *
from user_state import UserState

match_status_emoji = {
    3: "❓", # not confirmed, show first
    2: "☑️", # confirmed, show second
    1: "✅", # released, show third
    0: "🤼", # otherwise
}

def is_confirmed(state, clan_id, conf):
    return clan_id == state.clan.id and conf != None and conf != ""

def is_not_confirmed(state, clan_id, conf):
    return clan_id == state.clan.id and (conf == None or conf == "")

def match_status(state, match):
    if not_empty(match.conf1) and not_empty(match.conf2): return 1
    if is_not_confirmed(state, match.clan1_id, match.conf1) or is_not_confirmed(state, match.clan2_id, match.conf2): return 3
    if is_confirmed(state, match.clan1_id, match.conf1) or is_confirmed(state, match.clan2_id, match.conf2): return 2
    return 9

#############################
# process message from user #
#############################

async def home(state : UserState, cmd : SimpleNamespace):
    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != "HOME":
        state.push(Home(state))

    description = "\n".join([
        f"User: {state.user.name} ({state.user.role})",
        f"Clan: {state.clan.flag} {state.clan.tag}" if state.clan != None else None,
        f"",
        f"**__Legend__** (up to 5 matches, up to 2 weeks)",
        f"{match_status_emoji[3]} waiting for confirmation",
        f"{match_status_emoji[2]} waiting for opponent confirmation",
        f"{match_status_emoji[1]} confirmed by both parties (or admin)",
    ])

    # build match buttons
    matches : List[Match] = Matches.get(clan_id=state.clan.id, date_from=date.today() - timedelta(days = 14))
    matches.sort(key=lambda m: f"{match_status(state, m)}|{m.date}", reverse=True) # first, sort by status, then sort by date
    matchButtons = []
    for match in matches:
        if len(matchButtons) == 5: break
        # todo - when confirmed or released, do not show match confirmation
        matchButtons.append(Button(
            emoji = match_status_emoji[match_status(state, match)], 
            label = f"{match.date} {match.clan1} vs. {match.clan2}", 
            custom_id = NewMatch.cmd(state, option = NewMatchOption(next_step="CONFIRM", match=match))
        ))

    embed = discord.Embed(title="HeLO - Hell Let Loose ELO", description=description)
    new_own_match = Match(clan1_id=state.clan.id, clan1=state.clan.tag)
    components = [
        matchButtons,
        [
            Button(emoji = "🚹", label = "new match",
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=new_own_match, next_step="CLAN2"))), 
            Button(emoji = "🚻", label = "new coop match",
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=new_own_match, next_step="COOP1"))),
            Button(emoji = "🚼", label = "new match (admin)",
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=Match(), next_step="CLAN1"))), 
            Button(emoji = "🔎", label = "search match (admin)",
                   custom_id = SearchMatch.cmd(state)),
        ], [
#            Button(emoji = "🗂️", label = "select clan",
#                   custom_id = SelectClan.cmd(state, option = SelectClanOption(title = "Select Clan"))), 
#            Button(emoji = "🔎", label = "search clan",
#                   custom_id = SearchClan.cmd(state, option = SearchClanOption(title = "Search Clan"))),
            Button(emoji = "🗄️", label = "clans",
                   custom_id = ManageClans.cmd(state)),
            Button(emoji = "🗄️", label = "**users**",
                   custom_id = ManageUsers.cmd(state)),
            Button(emoji = "🗄️", label = "**events**",
                   custom_id = ManageEvents.cmd(state)),
        ], [
            Button(emoji = "🔒", label = "logout", custom_id = Login.cmd("LOGOUT")),
        ],
    ]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)    


