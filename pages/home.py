from datetime import datetime
import logging
from types import SimpleNamespace
import discord
from discord_components.component import Button
from database_models import Matches
from object_models import *


#############################
# process message from user #
#############################

async def home(state, cmd : SimpleNamespace):
    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != "HOME":
        state.push(Home(state))

    description = "\n".join([
        f"User: {state.user.name} ({state.user.role})",
        f"Clan: {state.clan.flag} {state.clan.tag}" if state.clan != None else None,
    ])

    # build match buttons
    matches = Matches.get(clan1_id=state.clan.id) # todo - what matches to load?
    matches.sort(lambda m: m.date)
    matchButtons = []
    for m in matches:
        if len(matchButtons) == 5: break
        matchButtons.append(Button(emoji = "🤼", label = f"{m.date} {m.clan1} vs. {m.clan2}", custom_id = f"MATCH"))
        # todo - add option for this match

    embed = discord.Embed(title="HeLO Screen Dummy", description=description)
    components = [
        matchButtons,
        [
            Button(emoji = "🗂️", label = "select clan",
                   custom_id = SelectClan.cmd(state, option = SelectClanOption(title = "Select Clan"))), 
            Button(emoji = "🔎", label = "search clan",
                   custom_id = SearchClan.cmd(state, option = SearchClanOption(title = "Search Clan"))),
            Button(emoji = "🗄️", label = "manage clans",
                   custom_id = ManageClans.cmd(state))
        ], [
            Button(emoji = "🚹", label = "new match",
                   custom_id = NewMatch.cmd(state, option = NewMatchOption(clan1 = state.clan.id, next_step = "CLAN2"))), 
            Button(emoji = "🚻", label = "new coop match",
                   custom_id = NewMatch.cmd(state, option = NewMatchOption(clan1 = state.clan.id, next_step = "COOP1"))), 
        ], [
            Button(emoji = "🔒", label = "logout", custom_id = Login.cmd("LOGOUT"))
        ],
    ]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)    


