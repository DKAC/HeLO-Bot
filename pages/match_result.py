import logging
from discord.embeds import Embed
from discord_components.component import Button
from discord_components.interaction import Interaction
from object_models import *
from messages.match_message import match_description
from env import *


#############################
# process message from user #
#############################

async def match_result(state, cmd : SimpleNamespace):
    logging.info(f"match_result_process_message: {cmd}")    
    
    if cmd.result != None:
        input = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result) 
    
        if type(cmd.result) != str and input.caps1 != None and input.side1 != None: # result has been selected
            return Return.cmd(state, result = { "caps1": input.caps1, "side1": input.side1 })
    
    state.push(MatchResult(state.current))
    
    embed = Embed(title = match_result_title, description = match_result_description(match_description(state)))
    
    components = [
        [            
            Button(label = "Allies", custom_id = MatchResult.cmd( state, side1 = "Allies1" ) ),
            Button(label = f"{emoji_five}:{emoji_zero}", custom_id = MatchResult.cmd( state, caps1 = 5, side1 = "Allies" ) ),
            Button(label = f"{emoji_four}:{emoji_one}", custom_id = MatchResult.cmd( state, caps1 = 4, side1 = "Allies" ) ),
            Button(label = f"{emoji_three}:{emoji_two}", custom_id = MatchResult.cmd( state, caps1 = 3, side1 = "Allies" ) )
        ], [            
            Button(label = "Allies", custom_id = MatchResult.cmd( state, side1 = "Allies2" ) ),
            Button(label = f"{emoji_two}:{emoji_three}", custom_id = MatchResult.cmd( state, caps1 = 2, side1 = "Allies" ) ),
            Button(label = f"{emoji_one}:{emoji_four}", custom_id = MatchResult.cmd( state, caps1 = 1, side1 = "Allies" ) ),
            Button(label = f"{emoji_zero}:{emoji_five}", custom_id = MatchResult.cmd( state, caps1 = 0, side1 = "Allies" ) )
        ], [            
            Button(label = "Axis", custom_id = MatchResult.cmd( state, side1 = "Axis1" ) ),
            Button(label = f"{emoji_five}:{emoji_zero}", custom_id = MatchResult.cmd( state, caps1 = 5, side1 = "Axis" ) ),
            Button(label = f"{emoji_four}:{emoji_one}", custom_id = MatchResult.cmd( state, caps1 = 4, side1 = "Axis" ) ),
            Button(label = f"{emoji_three}:{emoji_two}", custom_id = MatchResult.cmd( state, caps1 = 3, side1 = "Axis" ) )
        ], [            
            Button(label = "Axis", custom_id = MatchResult.cmd( state, side1 = "Axis2" ) ),
            Button(label = f"{emoji_two}:{emoji_three}", custom_id = MatchResult.cmd( state, caps1 = 2, side1 = "Axis" ) ),
            Button(label = f"{emoji_one}:{emoji_four}", custom_id = MatchResult.cmd( state, caps1 = 1, side1 = "Axis" ) ),
            Button(label = f"{emoji_zero}:{emoji_five}", custom_id = MatchResult.cmd( state, caps1 = 0, side1 = "Axis" ) )
        ], [
            Button(emoji=emoji_home, custom_id = Home.cmd(state))            
        ]
    ]
    
    if type(state.current.interaction) == Interaction:
        await state.current.respond(embed = embed, components = components)    
    else:
        await state.parent.interaction.message.delete()
        await state.current.interaction.author.send(content = "", embed = embed, components = components)    