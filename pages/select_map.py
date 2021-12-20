import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from data import *
from messages.match_message import match_description


async def select_map(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "map": cmd.result })    
    
    state.push(SelectMap(state.current))
    
    embed = Embed(title = "Map", description = f"{match_description(state)}**Select map**")
    
    components = [
        [            
            Button(label = maps[0]["tag"], custom_id = SelectMap.cmd( state, map = maps[0]["tag"] ) ),
            Button(label = maps[1]["tag"], custom_id = SelectMap.cmd( state, map = maps[1]["tag"] ) ),
            Button(label = maps[2]["tag"], custom_id = SelectMap.cmd( state, map = maps[2]["tag"] ) ),
        ], [            
            Button(label = maps[3]["tag"], custom_id = SelectMap.cmd( state, map = maps[3]["tag"] ) ),
            Button(label = maps[4]["tag"], custom_id = SelectMap.cmd( state, map = maps[4]["tag"] ) ),
            Button(label = maps[5]["tag"], custom_id = SelectMap.cmd( state, map = maps[5]["tag"] ) ),
        ], [            
            Button(label = maps[6]["tag"], custom_id = SelectMap.cmd( state, map = maps[6]["tag"] ) ),
            Button(label = maps[7]["tag"], custom_id = SelectMap.cmd( state, map = maps[7]["tag"] ) ),
            Button(label = maps[8]["tag"], custom_id = SelectMap.cmd( state, map = maps[8]["tag"] ) ),
        ], [            
            Button(label = maps[9]["tag"], custom_id = SelectMap.cmd( state, map = maps[9]["tag"] ) ),
            Button(label = maps[10]["tag"], custom_id = SelectMap.cmd( state, map = maps[10]["tag"] ) ),
            Button(emoji='🔼', custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    