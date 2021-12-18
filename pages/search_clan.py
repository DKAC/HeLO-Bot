import discord, logging
from data import *
from object_models import *
from pages.new_match import *


##################
# perform action #
##################
        
async def search_clan(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")

    if cmd.result != None:
        cmd.result["option_step"] = state.current.options[0].next_step
        return Return.cmd(state, cmd.result)
    
    input = state.current.options[cmd.input]
    state.push(SearchClan(state.current))
    state.current.callback = "SEARCH_CLAN"
    state.current.options = [input]
    
    embed = discord.Embed(title = input.title, description = f"{match_description(state)}**Enter clan search text below:**")
    components = [
        Button(emoji='🔼', custom_id = Home.cmd(state)),
    ]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)
    
    
async def search_clan_callback(state, input):    
    logging.info(f"input = {input}")
    clanSearch = { clan.tag.lower(): clan for clan in Clans.get()} # build map { "stdb": Clan(..."StDb"), ... }
    selected = [clan for clan in clanSearch.keys() if input.lower() in clan] # find by keys: "stdb", ...
    selected = [clanSearch[clan] for clan in selected] # map from key to value: "stdb" => Clan(..."StDb")
    logging.info(f"clans selected: {selected}")
    selected.sort(key=lambda clan: clan.tag)
    if len(selected) == 0:
        logging.info(f"no clan found with: {input}")
    else:
        return SelectClan.cmd(state, SelectClanOption(
            selected = selected, 
            is_showing_coop = state.current.options[0].is_showing_coop, 
            from_search = True,
            title = state.current.options[0].title
        ))
