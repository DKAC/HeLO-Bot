from typing import List
import discord, logging
from data import *
from object_models import *
from pages.new_match import *


##################
# perform action #
##################
        
async def search_match(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")

    input = state.current.options[cmd.input]
    state.push(SearchMatch(state))
    state.current.callback = "SEARCH_MATCH"
    state.current.options = [input]
    
    embed = discord.Embed(title = "Search Match", description = f"{match_description(state)}**Enter match id below (footer in match results):**")
    components = [Button(emoji='🔼', custom_id = Home.cmd(state))]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)
    
    
async def search_match_callback(state, input):    
    logging.info(f"input = {input}")
    matches : List[Match] = Matches.get(match_id=input)
    if len(matches) == 1:
        state.interaction = state.parent.interaction
        return NewMatch.cmd(state, option = NewMatchOption(next_step="CONFIRM", match=matches[0]))
    else:
        embed = discord.Embed(title = input.title, description = f"{match_description(state)}**Enter match id below (footer in match results):**")
        components = [Button(emoji='🔼', custom_id = Home.cmd(state))]
        await state.interaction.respond(type = 7, content = "", embed = embed, components = components)