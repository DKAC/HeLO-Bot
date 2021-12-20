import logging
from discord.embeds import Embed
from discord_components.component import Button
from object_models import *
from data import *
from messages.match_message import match_description


async def select_event(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "event": cmd.result })    
    
    state.push(SelectEvent(state.current))
    
    embed = Embed(title = "Event", description = f"{match_description(state)}**Select event**")
    
    # todo limit events to 20
    components = []
    for i in range(0, len(events)):
        if i % 5 == 0: components.append([])
        components[len(components) - 1].append(
            Button(label = events[i]["tag"], custom_id = SelectEvent.cmd( state, event = events[i]["tag"] ) )
        )
    components.append([
        Button(emoji='🔼', custom_id = Home.cmd(state))
    ])
    
    await state.current.respond(embed = embed, components = components)    