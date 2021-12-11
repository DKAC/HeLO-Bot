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
        cmd = state.current.options[cmd.input]
        state.push(NewMatch(state, clan1=Clans.get(cmd.clan1).tag, clan1_id=cmd.clan1, next_step=cmd.next_step))
    else:
        result = SimpleNamespace(**cmd.result)

        if state.current.next_step == "CLAN1":
            logging.info(f"CLAN1: {result.selected}")    
            state.current.clan1_id = result.selected    
            state.current.clan1 = Clans.get(result.selected).tag
            state.current.next_step = "COOP1" if not result.is_showing_coop else "CLAN2"

        elif state.current.next_step == "COOP1":
            logging.info(f"COOP1: {result.selected}")
            state.current.coop1_id = result.selected
            state.current.coop1 = Clans.get(result.selected).tag
            state.current.next_step = "CLAN2"
            
        elif state.current.next_step == "CLAN2":
            logging.info(f"CLAN2: {result.selected}")
            state.current.clan2_id = result.selected
            state.current.clan2 = Clans.get(result.selected).tag
            state.current.next_step = "COOP2" if not result.is_showing_coop else "RESULT"

        elif state.current.next_step == "COOP2":
            logging.info(f"COOP2: {result.selected}")
            state.current.coop2_id = result.selected
            state.current.coop2 = Clans.get(result.selected).tag
            state.current.next_step = "RESULT"
            
        elif state.current.next_step == "RESULT":
            logging.info(f"RESULT: {result.side1} {result.caps1}:{5 - result.caps1}")
            state.current.caps1 = result.caps1
            state.current.caps2 = 5 - result.caps1
            state.current.side1 = result.side1
            state.current.side2 = "Axis" if result.side1 == "Allies" else "Allies"
            state.current.next_step = "DATE"

        elif state.current.next_step == "DATE":
            logging.info(f"DATE: {result.date}")
            state.current.date = result.date
            state.current.next_step = "MAP"
            
        elif state.current.next_step == "MAP":
            logging.info(f"MAP: {result.map}")
            state.current.map = result.map
            state.current.next_step = "CONFIRM"
            
        elif state.current.next_step == "CONFIRM":
            logging.info(f"CONFIRM")            
            m = state.current
            match_id = Match.get_match_id(date=m.date, clan1=m.clan1, clan2=m.clan2)
            logging.info(f"write to DB: {match_id}")
            match = Match(match_id=match_id,
                clan1=m.clan1, clan1_id=m.clan1_id, coop1=m.coop1, coop1_id=m.coop1_id, clan2=m.clan2, clan2_id=m.clan2_id, coop2=m.coop2, coop2_id=m.coop2_id, side1=m.side1, side2=m.side2, caps1=m.caps1, caps2=m.caps2, map=m.map, date=m.date, duration=m.duration, factor=m.factor, event=m.event, conf1=state.user.userid, conf2=None
            )
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
    state = state.find(NewMatch)
    if state == None: return ""
    
    clans = Clans.get()
    
    # todo store id instead of tag
    dummy = Clan("dummy", tag = "???")
    clan1 = [clan for clan in clans if clan.id == state.clan1_id][0] if state.clan1 != None else dummy
    coop1 = [clan for clan in clans if clan.id == state.coop1_id][0] if state.coop1 != None else dummy
    clan2 = [clan for clan in clans if clan.id == state.clan2_id][0] if state.clan2 != None else dummy
    coop2 = [clan for clan in clans if clan.id == state.coop2_id][0] if state.coop2 != None else dummy
    
    s = "**New Match**\n"
    s += f"{clan1.flag} "   if clan1.flag != None else ""
    s += f"{clan1.tag}"
    s += " & "              if state.coop1 != None else ""
    s += f"{coop1.flag} "   if coop1.flag  != None else ""
    s += f"{coop1.tag}"     if state.coop1 != None else ""
    s += " vs. "
    s += f"{clan2.flag} "   if clan2.flag != None else ""
    s += f"{clan2.tag}"
    s += " & "              if state.coop2 != None else ""
    s += f"{coop2.flag} "   if coop2.flag != None else ""
    s += f"{coop2.tag}"     if state.coop2 != None else ""
    s += "\n"
    s += state.date if state.date != None else "???"
    s += "\n"
    s += state.map if state.map != None else "???"
    s += "\n"
    s += state.side1 if state.side1 != None else "???"
    s += " "
    s += str(state.caps1) if state.caps1 != None else "?"
    s += ":"
    s += str(state.caps2) if state.caps2 != None else "?"
    s += " "
    s += state.side2 if state.side2 != None else "???"
    s += "\n\n"
    return s