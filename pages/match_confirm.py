import logging
from discord.embeds import Embed
from discord_components.component import Button
from database_models import Clans, Matches
from object_models import *
from messages.match_message import match_description
from data import *
from user_state import UserState
from env import *


#############################
# process message from user #
#############################

async def match_confirm(state : UserState, cmd : SimpleNamespace):
    logging.info(f"{cmd}")
    
    if cmd.result == "CONFIRM":
        if state.parent.match.clan1_id == state.clan.id:
            return Return.cmd(state, result = { "conf1": state.userid })
        if state.parent.match.clan2_id == state.clan.id:
            return Return.cmd(state, result = { "conf2": state.userid })
    
    if cmd.result == "CONFIRM_ADMIN":
        if empty(state.parent.match.conf1) and empty(state.parent.match.conf2):
            return Return.cmd(state, result = { "conf1": state.userid, "conf2": state.userid })
        if empty(state.parent.match.conf1):
            return Return.cmd(state, result = { "conf1": state.userid })
        if empty(state.parent.match.conf2):
            return Return.cmd(state, result = { "conf2": state.userid })
    
    elif cmd.result == "DELETE":
        logging.info(f"delete from datebase: {state.parent.match.match_id}")
        Matches.delete(state, state.parent.match.id)
        return Home.cmd(state)
    
    elif cmd.result != None:
        # check if match has been edited
        try:
            match : Match = state.parent.match
            if "date" in cmd.result: 
                match.date = cmd.result["date"]
            if "caps1" in cmd.result: 
                match.caps1 = cmd.result["caps1"]
                match.caps2 = 5 - cmd.result["caps1"]
                if match.caps1 == 0 or match.caps2 == 0: match.duration = 90
            if "side1" in cmd.result:
                match.side1 = cmd.result.side1
                match.side2 = "Axis" if cmd.result.side1 == "Allies" else "Allies"
            if "duration" in cmd.result:
                match.duration = cmd.result["duration"]
            if "map" in cmd.result:
                match.map = cmd.result["map"]
            if "players" in cmd.result:
                match.players = cmd.result["players"]
            if "event" in cmd.result:
                match.event = cmd.result["event"]
                event = [event for event in events if event.tag == match.event]
                match.factor = event[0]["factor"] if len(event) > 0 else None
            if "selected" in cmd.result and "option_step" in cmd.result:
                if cmd.result["option_step"] == "CLAN1":
                    match.clan1_id = cmd.result["selected"]
                    match.clan1 = Clans.get(cmd.result["selected"]).tag
                elif cmd.result["option_step"] == "COOP1":
                    match.coop1_id = cmd.result["selected"]
                    match.coop1 = Clans.get(cmd.result["selected"]).tag
                elif cmd.result["option_step"] == "CLAN2":
                    match.clan2_id = cmd.result["selected"]
                    match.clan2 = Clans.get(cmd.result["selected"]).tag
                elif cmd.result["option_step"] == "COOP2":
                    match.coop2_id = cmd.result["selected"]
                    match.coop2 = Clans.get(cmd.result["selected"]).tag
        except:
            logging.info("?")
    
    if cmd.input != None:
        try:
            opt = state.current.options[cmd.input]
            logging.info(f"{opt}")
            logging.info(f"{state.current.match.match_id}")
            state.push(MatchConfirm(state))
        except:
            logging.info(f"No need to push another MatchConfirm")
    
    state.current.interaction = state.interaction if state.interaction != None else state.parent.interaction
    
    embed = Embed(title = match_confirm_title, description = match_confirm_description(match_description(state)))
    
    components = [
        [
            Button(emoji=emoji_clan, custom_id = SearchClan.cmd(state, SearchClanOption(title = match_confirm_clan1_title, next_step = "CLAN1"))),
            Button(emoji=emoji_coop, custom_id = SearchClan.cmd(state, SearchClanOption(title = match_confirm_coop1_title, next_step = "COOP1"))),
            Button(label=match_confirm_vs, custom_id = MatchConfirm.cmd(state)),
            Button(emoji=emoji_clan, custom_id = SearchClan.cmd(state, SearchClanOption(title = match_confirm_clan2_title, next_step = "CLAN2"))),
            Button(emoji=emoji_coop, custom_id = SearchClan.cmd(state, SearchClanOption(title = match_confirm_coop2_title, next_step = "COOP2"))),
        ], [
            Button(emoji=emoji_event, custom_id = SelectEvent.cmd(state, next_step="CONFIRM")),
            Button(emoji=emoji_date, custom_id = MatchDate.cmd(state, next_step="CONFIRM")),
            Button(emoji=emoji_map, custom_id = SelectMap.cmd(state, next_step="CONFIRM")),
        ], [
            Button(emoji=emoji_score, custom_id = MatchResult.cmd(state, next_step="CONFIRM")),
            Button(emoji=emoji_duration, custom_id = MatchDuration.cmd(state, next_step="CONFIRM") 
                   if state.parent.match.caps1 != 0 and state.parent.match.caps2 != 0 else MatchConfirm.cmd(state)),
            Button(emoji=emoji_players, custom_id = MatchPlayers.cmd(state, next_step="CONFIRM")),
        ], [b for b in [
            Button(emoji=emoji_ok, custom_id = MatchConfirm.cmd(state, confirm = "CONFIRM" )) if confirmed(state.parent.match, state) else None,
            Button(emoji=emoji_confirm_admin, custom_id = MatchConfirm.cmd(state, confirm = "CONFIRM_ADMIN" )), # TODO if role == admin and not fully confirmed
            Button(emoji=emoji_delete, custom_id = MatchConfirm.cmd(state, confirm = "DELETE" )), # TODO if role == admin
            Button(emoji=emoji_home, custom_id = Home.cmd(state)),
            ] if b != None
        ]
    ]
    
    await state.current.respond(embed = embed, components = components)
    
def confirmed(match : Match, state : UserState):
    if state.clan.id == match.clan1_id and match.conf1 == None: return True
    if state.clan.id == match.clan2_id and match.conf2 == None: return True
    return False