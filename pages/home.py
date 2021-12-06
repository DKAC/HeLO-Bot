import logging
from types import SimpleNamespace
import discord
from discord_components.component import Button
from object_models import *


#############################
# process message from user #
#############################

async def home(state, cmd : SimpleNamespace):
    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != "HOME":
        state.push(Home(state))

    clan_tag = state.user.clan.tag if state.user.clan != None else "?"
    embed = discord.Embed(title="HeLO Screen Dummy", description=f"Clan: {clan_tag}")
    components = [
        [
            Button(emoji = "🗂️", label = "select clan",
                   custom_id = SelectClan.cmd(state, option = SelectClanOption(title = "Select Clan", is_showing_coop = True))), 
            Button(emoji = "🔎", label = "search clan",
                   custom_id = SearchClan.cmd(state, option = SearchClanOption(title = "Search Clan", is_showing_coop = True))),
            Button(emoji = "🗄️", label = "manage clans",
                   custom_id = ManageClans.cmd(state))
        ], [
            Button(emoji = "🚹", label = "new match",
                   custom_id = NewMatch.cmd(state, option = NewMatchOption(clan1 = state.user.clan.tag, next_step = "CLAN2"))), # todo switch to id
            Button(emoji = "🚻", label = "new coop match",
                   custom_id = NewMatch.cmd(state, option = NewMatchOption(clan1 = state.user.clan.tag, next_step = "COOP1"))) # todo switch to id
        ], [
            Button(emoji = "🔒", label = "logout", custom_id = Login.cmd("LOGOUT"))
        ],
    ]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)    


