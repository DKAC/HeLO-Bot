import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from messages.match_message import match_description
from env import *

#############################
# process message from user #
#############################

async def match_duration(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "duration": cmd.result })    
    
    state.push(MatchDuration(state.current))
    
    embed = Embed(title = match_duration_title, description = match_duration_description(match_description(state)))
    
    components = [
        [
            Button(label = "90", custom_id = MatchDuration.cmd( state, duration = 90 ) ),
            Button(label = "85", custom_id = MatchDuration.cmd( state, duration = 85 ) ),
            Button(label = "80", custom_id = MatchDuration.cmd( state, duration = 80 ) ),
            Button(label = "75", custom_id = MatchDuration.cmd( state, duration = 75 ) ),
        ], [            
            Button(label = "70", custom_id = MatchDuration.cmd( state, duration = 70 ) ),
            Button(label = "65", custom_id = MatchDuration.cmd( state, duration = 65 ) ),
            Button(label = "60", custom_id = MatchDuration.cmd( state, duration = 60 ) ),
            Button(label = "55", custom_id = MatchDuration.cmd( state, duration = 55 ) ),
        ], [            
            Button(label = "50", custom_id = MatchDuration.cmd( state, duration = 50 ) ),
            Button(label = "45", custom_id = MatchDuration.cmd( state, duration = 45 ) ),
            Button(label = "40", custom_id = MatchDuration.cmd( state, duration = 40 ) ),
            Button(label = "35", custom_id = MatchDuration.cmd( state, duration = 35 ) ),
        ], [            
            Button(label = "30", custom_id = MatchDuration.cmd( state, duration = 30 ) ),
            Button(label = "25", custom_id = MatchDuration.cmd( state, duration = 25 ) ),
            Button(label = "20", custom_id = MatchDuration.cmd( state, duration = 20 ) ),
            Button(label = "15", custom_id = MatchDuration.cmd( state, duration = 15 ) ),
        ], [            
            Button(emoji=emoji_home, custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    