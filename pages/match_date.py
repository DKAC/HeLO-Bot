import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from messages.match_message import match_description
from env import *

#############################
# process message from user #
#############################

async def match_date(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "date": cmd.result })    
    
    state.push(MatchDate(state.current))
    
    embed = Embed(title = match_date_title, description = match_date_description(match_description(state)))
    
    components = [
        [            
            Button(label = match_date_label(0), custom_id = MatchDate.cmd( state, date = match_date_iso(0) ) ),
            Button(label = match_date_label(1), custom_id = MatchDate.cmd( state, date = match_date_iso(1) ) ),
            Button(label = match_date_label(2), custom_id = MatchDate.cmd( state, date = match_date_iso(2) ) )
        ], [            
            Button(label = match_date_label(3), custom_id = MatchDate.cmd( state, date = match_date_iso(3) ) ),
            Button(label = match_date_label(4), custom_id = MatchDate.cmd( state, date = match_date_iso(4) ) ),
            Button(label = match_date_label(5), custom_id = MatchDate.cmd( state, date = match_date_iso(5) ) )
        ], [            
            Button(label = match_date_label(6), custom_id = MatchDate.cmd( state, date = match_date_iso(6) ) ),
            Button(label = match_date_label(7), custom_id = MatchDate.cmd( state, date = match_date_iso(7) ) ),
            Button(label = match_date_label(8), custom_id = MatchDate.cmd( state, date = match_date_iso(8) ) )
        ], [            
            Button(label = match_date_label(9), custom_id = MatchDate.cmd( state, date = match_date_iso(9) ) ),
            Button(label = match_date_label(10), custom_id = MatchDate.cmd( state, date = match_date_iso(10) ) ),
            Button(label = match_date_label(11), custom_id = MatchDate.cmd( state, date = match_date_iso(11) ) )
        ], [            
            Button(label = match_date_label(12), custom_id = MatchDate.cmd( state, date = match_date_iso(12) ) ),
            Button(label = match_date_label(13), custom_id = MatchDate.cmd( state, date = match_date_iso(13) ) ),
            Button(emoji = emoji_home, custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    