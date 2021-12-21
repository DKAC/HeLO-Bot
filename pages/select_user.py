import logging
from types import SimpleNamespace
from object_models import *
from discord import Embed
from discord_components import Button

async def select_user(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
        
    if cmd.input != None:
        opt = state.current.options[cmd.input]
        if len(opt.selected) == 1:
            return Return.cmd(state, result = { "field": EditUser.name, "userid": opt.selected[0] })
    
        state.push(SelectUser(state))
        state.current.interaction = state.parent.interaction
        
        embed = Embed(title = "Select User")
        
        components = []
        row = []
        for user in opt.selected:
            row.append(Button(label = user.name, custom_id = SelectUser.cmd(state, SelectUserOption(selected = [user.userid]))))

            if len(row) == 5:
                components.append(row)
                row = []
                
        components.append(row)
                    
    await state.current.respond(embed = embed, components = components)    
    
