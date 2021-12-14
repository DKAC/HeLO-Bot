import logging
from database_models import Clans, Matches, Match
from pages.select_clan import *
from object_models import *


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
            if match.clan1_id == state.clan.id: state.current.match.conf1 = state.user.userid
            if match.clan2_id == state.clan.id: state.current.match.conf2 = state.user.userid
                
            # todo - remove this, when everything is complete
            state.current.match.duration = "90"

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
    
    if state.current.next_step == "DATE": 
        return MatchDate.cmd(state)
    
    if state.current.next_step == "MAP": 
        return SelectMap.cmd(state)
    
    if state.current.next_step == "CONFIRM": 
        return MatchConfirm.cmd(state)
    
    if state.current.next_step == "DONE":  
        return Home.cmd(state)


def match_description(state):
    new_match = state.find(NewMatch)
    if new_match == None: return ""
    
    match = new_match.match
    
    clans = Clans.get()
    
    # todo store id instead of tag
    dummy = Clan("dummy", tag = "???")
    clan1 = [clan for clan in clans if clan.id == match.clan1_id][0] if match.clan1 != None and match.clan1 != "" else dummy
    coop1 = [clan for clan in clans if clan.id == match.coop1_id][0] if match.coop1 != None and match.coop1 != "" else dummy
    clan2 = [clan for clan in clans if clan.id == match.clan2_id][0] if match.clan2 != None and match.clan2 != "" else dummy
    coop2 = [clan for clan in clans if clan.id == match.coop2_id][0] if match.coop2 != None and match.coop2 != "" else dummy
    
    s = "**Edit Match**" if not_empty(match.match_id) else "**New Match**"
    s += "\n"
    s += f"{clan1.flag} "   if not_empty(clan1.flag)  else ""
    s += f"{clan1.tag}"
    s += " & "              if not_empty(match.coop1) else ""
    s += f"{coop1.flag} "   if not_empty(coop1.flag)  else ""
    s += f"{coop1.tag}"     if not_empty(match.coop1) else ""
    s += " vs. "
    s += f"{clan2.flag} "   if not_empty(clan2.flag)  else ""
    s += f"{clan2.tag}"
    s += " & "              if not_empty(match.coop2) else ""
    s += f"{coop2.flag} "   if not_empty(coop2.flag)  else ""
    s += f"{coop2.tag}"     if not_empty(match.coop2) else ""
    s += "\n"
    s += match.date if match.date != None else "???"
    s += "\n"
    s += match.map if not_empty(match.map) else "???"
    s += "\n"
    s += match.side1 if not_empty(match.side1) else "???"
    s += " "
    s += str(match.caps1) if match.caps1 != None else "?"
    s += ":"
    s += str(match.caps2) if match.caps2 != None else "?"
    s += " "
    s += match.side2 if not_empty(match.side2) else "???"
    s += "\n\n"
    return s