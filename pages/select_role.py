import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from messages.match_message import match_description


async def select_role(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "role": cmd.result })    
    
    state.push(SelectRole(state.current))
    
    embed = Embed(title = "Role", description = f"{match_description(state)}**Select role**")
    
    components = [
        [            
            Button(label = "admin", custom_id = SelectRole.cmd( state, role = "admin" ) ),
            Button(label = "representative", custom_id = SelectRole.cmd( state, role = "representative" ) ),
            Button(label = "member", custom_id = SelectRole.cmd( state, role = "member" ) ),
        ], [            
            Button(emoji='🔼', custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    