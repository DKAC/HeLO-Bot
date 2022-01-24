import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from messages.match_message import match_description
from env import *

#############################
# process message from user #
#############################

async def match_players(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "players": cmd.result })    
    
    state.push(MatchPlayers(state.current))
    
    embed = Embed(title = match_players_title, description = match_players_description(match_description(state)))
    
    components = [
        [
            Button(label = "50", custom_id = MatchPlayers.cmd( state, players = 50 ) ),
            Button(label = "45", custom_id = MatchPlayers.cmd( state, players = 45 ) ),
            Button(label = "40", custom_id = MatchPlayers.cmd( state, players = 40 ) ),
            Button(label = "35", custom_id = MatchPlayers.cmd( state, players = 35 ) ),
        ], [            
            Button(label = "30", custom_id = MatchPlayers.cmd( state, players = 30 ) ),
            Button(label = "25", custom_id = MatchPlayers.cmd( state, players = 25 ) ),
            Button(label = "20", custom_id = MatchPlayers.cmd( state, players = 20 ) ),
            Button(label = "15", custom_id = MatchPlayers.cmd( state, players = 15 ) ),
        ], [            
            Button(emoji=emoji_home, custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    