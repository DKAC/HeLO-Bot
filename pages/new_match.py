import logging

from database_models import Clans, Matches, Match
from messages.match_message import *
from messages.score_message import ScoresMessage
from pages.select_clan import *
from object_models import *
from env import *

#############################
# process message from user #
#############################

async def new_match(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    

    if cmd.result == None:
        opt = state.current.options[cmd.input]
        opt.clan1 = Clans.get(opt.clan1).tag if opt.clan1_id != None else None
        state.push(NewMatch(state, next_step=opt.next_step, match=opt.match))
    else:
        logging.info(f"{state.current.next_step}")
        result = SimpleNamespace(**cmd.result)
        match = state.current.match
        if state.current.next_step == "CLAN1":
            logging.info(f"CLAN1: {result.selected}")
            match.clan1_id = result.selected
            match.clan1 = Clans.get(result.selected).tag
            state.current.next_step = "COOP1" if not result.is_showing_coop else "CLAN2"

        elif state.current.next_step == "COOP1":
            logging.info(f"COOP1: {result.selected}")
            match.coop1_id = result.selected
            match.coop1 = Clans.get(result.selected).tag
            state.current.next_step = "CLAN2"
            
        elif state.current.next_step == "CLAN2":
            logging.info(f"CLAN2: {result.selected}")
            match.clan2_id = result.selected
            match.clan2 = Clans.get(result.selected).tag
            state.current.next_step = "COOP2" if not result.is_showing_coop else "RESULT"

        elif state.current.next_step == "COOP2":
            logging.info(f"COOP2: {result.selected}")
            match.coop2_id = result.selected
            match.coop2 = Clans.get(result.selected).tag
            state.current.next_step = "RESULT"
            
        elif state.current.next_step == "RESULT":
            logging.info(f"RESULT: {result.side1} {result.caps1}:{5 - result.caps1}")
            match.caps1 = result.caps1
            match.caps2 = 5 - result.caps1
            match.side1 = result.side1
            match.side2 = "Axis" if result.side1 == "Allies" else "Allies"
            if match.caps1 == 5 or match.caps2 == 5:
                match.duration = 90
                state.current.next_step = "PLAYERS"
            else:
                state.current.next_step = "DURATION"

        elif state.current.next_step == "DURATION":
            logging.info(f"DURATION: {result.duration}")
            match.duration = result.duration
            state.current.next_step = "PLAYERS"
            
        elif state.current.next_step == "PLAYERS":
            logging.info(f"PLAYERS: {result.players}")
            match.players = result.players
            state.current.next_step = "EVENT"
            
        elif state.current.next_step == "EVENT":
            logging.info(f"EVENT: {result.event}")
            match.event = result.event
            state.current.next_step = "DATE"
            
        elif state.current.next_step == "DATE":
            logging.info(f"DATE: {result.date}")
            match.date = result.date
            state.current.next_step = "MAP"
            
        elif state.current.next_step == "MAP":
            logging.info(f"MAP: {result.map}")
            match.map = result.map
            state.current.next_step = "CONFIRM"
            
        elif state.current.next_step == "CONFIRM":
            logging.info(f"CONFIRM")
            if "conf1" in cmd.result: match.conf1 = cmd.result["conf1"]
            if "conf2" in cmd.result: match.conf2 = cmd.result["conf2"]
                
            match_id = Match.get_match_id(date=match.date, clan1=match.clan1, clan2=match.clan2)
            if match.match_id != None:
                if match.match_id == match_id:
                    logging.info(f"update match in DB: {match.match_id}")
                    Matches.update(state, state.current.match)
                else:
                    logging.info(f"recreate match in DB: {match.match_id} -> {match_id}")
                    Matches.delete(state, match.id)
                    state.current.match.match_id = match_id
                    Matches.create(state, state.current.match)
            else:
                logging.info(f"create match in DB: {match_id}")
                match.match_id = match_id
                Matches.create(state, match)

            logging.info(f"create/update match message: {match.conf1}, {match.conf2}")
            await MatchMessage.send(state)

            logging.info(f"create/update scores message")
            await ScoresMessage.send(state)

            state.current.next_step = "DONE"
            
    if state.current.next_step == "CLAN1": 
        return SearchClan.cmd(state, option = SearchClanOption( title = "Search 1. Clan", is_showing_coop = True ))
    
    if state.current.next_step == "COOP1": 
        return SearchClan.cmd(state, option = SearchClanOption( title = "Search 1. Clans Coop partner" ))
    
    if state.current.next_step == "CLAN2":  
        return SearchClan.cmd(state, option = SearchClanOption( title = "Search 2. Clan", is_showing_coop = True ))    
    
    if state.current.next_step == "COOP2":  
        return SearchClan.cmd(state, option = SearchClanOption( title = "Search 2. Clans Coop partner" ))
    
    if state.current.next_step == "RESULT": 
        return MatchResult.cmd(state)
    
    if state.current.next_step == "DURATION": 
        return MatchDuration.cmd(state)
    
    if state.current.next_step == "PLAYERS": 
        return MatchPlayers.cmd(state)
    
    if state.current.next_step == "EVENT": 
        return SelectEvent.cmd(state)
    
    if state.current.next_step == "DATE": 
        return MatchDate.cmd(state)
    
    if state.current.next_step == "MAP": 
        return SelectMap.cmd(state)
    
    if state.current.next_step == "CONFIRM": 
        return MatchConfirm.cmd(state)
    
    if state.current.next_step == "DONE":  
        return Home.cmd(state)


