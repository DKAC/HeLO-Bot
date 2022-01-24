import logging
from types import SimpleNamespace
from object_models import *
from discord import Embed
from discord_components import Button

async def select_factor(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
        

    if cmd.input != None:
        return Return.cmd(state, result = { "field": "SELECT_FACTOR", "factor": cmd.input })    
    
    state.push(SelectFactor(state))
    
    embed = Embed(title = "Select Factor")

    factors = [
        0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 0.9, 1.0,
        1.1, 1.2, 1.3, 1.4, 1.5,
        1.6, 1.7, 1.8, 1.9, 2.0,
        "home"
    ]
      
    components = []
    row = []
    for n in factors:
        if len(row) == 5:
            components.append(row)
            row = []

        if n == "home": 
            row.append(Button(emoji = "🔼", custom_id = Home.cmd(state)))
        else:
            row.append(Button(label = str(n), custom_id = SelectFactor.cmd(state, n)))

    components.append(row)
    
    await state.current.respond(embed = embed, components = components)    
    
