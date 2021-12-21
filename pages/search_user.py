import discord, logging
from data import *
from database_models import Users
from object_models import *
from pages.new_match import *


##################
# perform action #
##################
        
async def search_user(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")

    if cmd.result != None:
        cmd.result["option_step"] = state.current.options[0].next_step
        return Return.cmd(state, cmd.result)
    
    input = state.current.options[cmd.input]
    state.push(SearchUser(state.current))
    state.current.callback = "SEARCH_USER"
    state.current.options = [input]
    
    embed = discord.Embed(title = input.title, description = f"{match_description(state)}**Enter user search text below:**")
    components = [
        Button(emoji='🔼', custom_id = Home.cmd(state)),
    ]
    await state.interaction.respond(type = 7, content = "", embed = embed, components = components)
    
    
async def search_user_callback(state, input):    
    logging.info(f"input = {input}")
    selected = Users.get(name_like=input)
    logging.info(f"users selected: {selected}")
    selected.sort(key=lambda user: user.name)
    if len(selected) == 0:
        logging.info(f"no user found with: {input}")
    else:
        return SelectUser.cmd(state, SelectUserOption(
            selected = selected, 
            from_search = True,
            title = state.current.options[0].title
        ))
