import logging
from discord.embeds import Embed
from discord_components.component import Button
from database_models import Matches
from object_models import *
from pages.new_match import match_description


#############################
# process message from user #
#############################

async def match_confirm(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result == "CONFIRM":
        return Return.cmd(state, result = { "conf1": state.userid })
    
    elif cmd.result == "DELETE":
        logging.info(f"delete from datebase: {state.parent.match.match_id}")
        Matches.delete(state, state.parent.match.id)
        return Home.cmd(state)
    
    elif cmd.result != None:
        # check if match has been edited
        try:
            if "date" in cmd.result: 
                state.parent.match.date = cmd.result["date"]
            if "caps1" in cmd.result: 
                state.parent.match.caps1 = cmd.result["caps1"]
                state.parent.match.caps2 = 5 - cmd.result["caps1"]
            if "side1" in cmd.result:
                state.parent.match.side1 = cmd.result.side1
                state.parent.match.side2 = "Axis" if cmd.result.side1 == "Allies" else "Allies"
            if "duration" in cmd.result:
                state.parent.match.duration = cmd.result.duration
            if "map" in cmd.result:
                state.parent.match.map = cmd.result["map"]
        except:
            logging.info("?")
    
    if cmd.input != None:
        opt = state.current.options[cmd.input]
        logging.info(f"{opt}")
        logging.info(f"{state.current.match.match_id}")
        state.push(MatchConfirm(state.current))
    else:
        state.current.interaction = state.interaction
    
    embed = Embed(title = "Match confirmation", description = f"{match_description(state)}**Confirm match (your user id will be added to the match data)**")
    
    components = [
        [
            Button(emoji='🗓️', custom_id = MatchDate.cmd(state, next_step="CONFIRM")),
            Button(emoji='5️⃣', custom_id = MatchResult.cmd(state, next_step="CONFIRM")),
            Button(emoji='⏱️', custom_id = "--"),#MatchDuration.cmd(state)),
            Button(emoji='🗺️', custom_id = SelectMap.cmd(state, next_step="CONFIRM"))
        ], [
            Button(emoji='🆗', custom_id = MatchConfirm.cmd(state, confirm = "CONFIRM" )),
            Button(emoji='🗑️', custom_id = MatchConfirm.cmd(state, confirm = "DELETE" )),
            Button(emoji='🔼', custom_id = Home.cmd(state))
        ]
    ]
    
    await state.current.respond(embed = embed, components = components)    