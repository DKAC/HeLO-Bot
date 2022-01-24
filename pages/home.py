from datetime import date, timedelta
import logging
from types import SimpleNamespace
from typing import List
import discord
from discord_components.component import Button
from database_models import Match, Matches
from object_models import *
from user_state import UserState
from env import *

match_status_emoji = {
    3: emoji_status_not_confirmed, # not confirmed, show first
    2: emoji_status_confirmed, # confirmed, show second
    1: emoji_status_released, # released, show third
    0: emoji_status_other, # otherwise
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

    embed = discord.Embed(title=home_title, description=home_description(state))
    components = []

    # build match buttons
    matches : List[Match] = Matches.get(clan_id=state.clan.id, date_from=date.today() - timedelta(days = 14))
    matches.sort(key=lambda m: f"{match_status(state, m)}|{m.date}", reverse=True) # first, sort by status, then sort by date
    matchButtons = []
    for match in matches:
        if len(matchButtons) == 5: break
        # todo - when confirmed or released, do not show match confirmation
        matchButtons.append(Button(
            emoji = match_status_emoji[match_status(state, match)], 
            label = home_match_status(match), 
            custom_id = NewMatch.cmd(state, option = NewMatchOption(next_step="CONFIRM", match=match))
        ))
    if matchButtons != []: components.append(matchButtons)

    new_own_match = Match(clan1_id=state.clan.id, clan1=state.clan.tag)
    components.append(
        [
            Button(emoji = emoji_clan, label = home_new_match,
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=new_own_match, next_step="CLAN2"))), 
            Button(emoji = emoji_coop, label = home_new_coop_match,
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=new_own_match, next_step="COOP1"))),
            Button(emoji = emoji_clan_admin, label = home_new_match_admin,
                   custom_id = NewMatch.cmd(state, option=NewMatchOption(match=Match(), next_step="CLAN1"))), 
            Button(emoji = "🔎", label = home_search_match_admin,
                   custom_id = SearchMatch.cmd(state)),
        ])
    components.append([
#            Button(emoji = "🗂️", label = "select clan", custom_id = SelectClan.cmd(state, option = SelectClanOption(title = "Select Clan"))), 
#            Button(emoji = "🔎", label = "search clan", custom_id = SearchClan.cmd(state, option = SearchClanOption(title = "Search Clan"))),
            Button(emoji = emoji_data, label = home_clans, custom_id = ManageClans.cmd(state)),
            Button(emoji = emoji_data, label = home_users, custom_id = ManageUsers.cmd(state)),
            Button(emoji = emoji_data, label = home_events, custom_id = ManageEvents.cmd(state)),
        ])
    components.append([
            Button(emoji = "🔒", label = home_logout, custom_id = Login.cmd("LOGOUT")),
        ],
    )
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)    


