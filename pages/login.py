from types import SimpleNamespace
import discord, logging
from discord.errors import NotFound
from discord_components.component import Button
from discord_components.interaction import Interaction
from database_models import Auth, Clans
from pages.home import * 
from data import * 
from object_models import *
from env import *


#############################
# process message from user #
#############################

async def login(state, cmd : SimpleNamespace):
    logging.info(f"{cmd if type(cmd.input) != int else 'numpad button pressed'}")

    state.push(Login(state), when = state.current == None)    

    inputs = {
        "CLEAR" :   clear_perform,
        "AUTH":     auth_perform,
        "LOGIN":    login_perform,
        "LOGOUT":   logout_perform
    }

    await inputs.get(cmd.input, numpad)(state, cmd)


async def numpad(state, cmd):
    if type(cmd.input) == int:
        state.current.input += str(cmd.input)
    else:
        logging.info(f"No valid command: {cmd.input}")
        return

    await state.current.respond()


async def clear_perform(state, cmd):
    logging.info(f"clear numpad input")
    state.current.input = ""
    await state.current.respond()
        

async def login_perform(state, cmd):
    logging.info(f"show numpad")
    state.current.input = ""
    
    title = login_title
    if state.current.title != None: title = state.current.title
    
    embed = discord.Embed(title=title, description=login_description)
    components = [[
        Button(emoji=emoji_one, custom_id=Login.cmd(1)),
        Button(emoji=emoji_two, custom_id=Login.cmd(2)),   
        Button(emoji=emoji_three, custom_id=Login.cmd(3)),   
    ], [
        Button(emoji=emoji_four, custom_id=Login.cmd(4)),
        Button(emoji=emoji_five, custom_id=Login.cmd(5)),   
        Button(emoji=emoji_six, custom_id=Login.cmd(6)),   
    ], [
        Button(emoji=emoji_seven, custom_id=Login.cmd(7)),
        Button(emoji=emoji_eight, custom_id=Login.cmd(8)),   
        Button(emoji=emoji_nine, custom_id=Login.cmd(9)),   
    ], [
        Button(emoji=emoji_back, custom_id=Login.cmd("CLEAR")),
        Button(emoji=emoji_zero, custom_id=Login.cmd(0)),   
        Button(emoji=emoji_ok, custom_id=Login.cmd("AUTH")),   
    ]]
    if type(state.current.interaction) == Interaction:
        await state.current.respond(embed = embed, components = components)
    else:
        if state.current.message != None:
            await state.current.message.channel.send(embed = embed, components = components)
        else:
            # todo - send message by user id
            logging.warning("TODO")
        

async def auth_perform(state, cmd : SimpleNamespace):
    logging.info(f"authenticate user {cmd}")
    response = Auth.post(state)
    
    if response != None and response.status_code == 200:
        # read user data
        state.user = SimpleNamespace(**json.loads(response.content))
        # read clan data for the users clan
        if state.user.clan != None: 
            state.clan = Clans.get(state.user.clan)
            
        await home(state, SimpleNamespace(**{ "action": "HOME" }))
        
    else:
        state.current.title = login_failed
        await login_perform(state, cmd)


async def logout_perform(state, cmd : SimpleNamespace):
    logging.info(f"logout and clear user state")
    interaction = state.interaction
    state.clear()
    embed = discord.Embed(title=logout_title, description=logout_description)
    components = [ Button(emoji = emoji_login, label = logout_login, custom_id = Login.cmd("LOGIN")) ]
    await interaction.respond(type = 7, content = "", embed = embed, components = components)
