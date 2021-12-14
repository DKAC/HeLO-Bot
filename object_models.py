import json
import logging
from types import SimpleNamespace
from object_state import *
from database_models import Clan


#########################################################################################
# state objects to hold the state of the current and previous steps                     #
# option objects to hold the parameters when executing the next step                    #
#########################################################################################

    
class Login(ObjectState):
    name = "LOGIN"
    def __init__(self, state): 
        ObjectState.__init__(self, Login.name, state)

    def cmd(input = None) -> str:
        return json.dumps({ "action": Login.name, "input": input, "result": None })
        
        
class Logout(ObjectState):
    name = "LOGOUT"
    def __init__(self, state): 
        ObjectState.__init__(self, Logout.name, state)
    

class Home(ObjectState):
    name = "HOME"
    def __init__(self, state): 
        ObjectState.__init__(self, Home.name, state)

    def cmd(state) -> str:
        return json.dumps({ "action": Home.name, "input": None, "result": None })

        
class ManageEvents(ObjectState):
    name = "MANAGE_EVENTS"
    def __init__(self, state):
        ObjectState.__init__(self, ManageEvents.name, state)

    def cmd(state) -> str:
        return json.dumps({ "action": ManageEvents.name, "input": None, "result": None, "callback": None })

        
class ManageUsers(ObjectState):
    name = "MANAGE_USERS"
    def __init__(self, state):
        ObjectState.__init__(self, ManageUsers.name, state)

    def cmd(state) -> str:
        return json.dumps({ "action": ManageUsers.name, "input": None, "result": None, "callback": None })

        
class ManageClans(ObjectState):
    name = "MANAGE_CLANS"
    def __init__(self, state):
        ObjectState.__init__(self, ManageClans.name, state)

    def cmd(state) -> str:
        return json.dumps({ "action": ManageClans.name, "input": None, "result": None, "callback": None })

        
class AddClan(ObjectState):
    name = "ADD_CLAN"
    def __init__(self, state, next_step, title): 
        ObjectState.__init__(self, AddClan.name, state)
        self.next_step = next_step
        self.title = title

    def cmd(state) -> str:
        return json.dumps({ "action": AddClan.name, "input": None, "result": None, "callback": None })

        
class EditClanOption:
    def __init__(self, next_step = None, title = ""):
        self.next_step = next_step
        self.title = title

    def __repr__(self): return json.dumps(self.__dict__)


class EditClan(ObjectState):
    name = "EDIT_CLAN"
    def __init__(self, state, next_step, title): 
        ObjectState.__init__(self, EditClan.name, state)
        self.next_step = next_step        
        self.title = title
        self.clan : Clan

    def cmd(state, confirm = None, option = EditClanOption()) -> str:
        return json.dumps({ "action": EditClan.name, "input": state.current.last_option(), "result": confirm })


class DeleteClanOption:
    def __init__(self, next_step = None, title = ""):
        self.next_step = next_step
        self.title = title

    def __repr__(self): return json.dumps(self.__dict__)


class DeleteClan(ObjectState):
    name = "DELETE_CLAN"
    def __init__(self, state, next_step): 
        ObjectState.__init__(self, DeleteClan.name, state)
        self.next_step = next_step

    def cmd(state, confirm = None, option = DeleteClanOption()) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": DeleteClan.name, "input": state.current.last_option(), "result": confirm })


class DeleteClanConfirmOption:
    def __init__(self, clan = None):
        self.clan = clan

    def __repr__(self): return json.dumps(self.__dict__)
        
                
class DeleteClanConfirm(ObjectState):
    name = "DELETE_CLAN_CONFIRM"
    def __init__(self, state): 
        ObjectState.__init__(self, DeleteClanConfirm.name, state)

    def cmd(state, confirm = None, option = DeleteClanOption()) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": DeleteClanConfirm.name, "input": state.current.last_option(), "result": confirm })

        
class SelectFlag(ObjectState):
    name = "SELECT_FLAG"
    def __init__(self, state): 
        ObjectState.__init__(self, SelectFlag.name, state)

    def cmd(state, input = None, option = None) -> str:
        return json.dumps({ "action": SelectFlag.name, "input": input, "result": None })
    

class SelectClanOption:
    def __init__(self, selected = None, next_step = None, is_showing_coop = False, from_search = False, title = ""):
        self.selected = selected
        self.is_showing_coop = is_showing_coop
        self.from_search = from_search
        self.next_step = next_step
        self.title = title
            
    def __repr__(self):               
        return json.dumps({ "selected": None if self.selected == None else [s.tag for s in self.selected], "is_showing_coop": self.is_showing_coop, "from_search": self.from_search, "next_step": self.next_step, "title": self.title})

      
class SelectClan(ObjectState):
    name = "SELECT_CLAN"
    def __init__(self, state): 
        ObjectState.__init__(self, SelectClan.name, state)

    def cmd(state, option = SelectClanOption()) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": SelectClan.name, "input": state.current.last_option(), "result": None } )


class SearchClanOption:
    def __init__(self, selected = None, next_step = None, is_showing_coop = False, title = ""):
        self.is_showing_coop = is_showing_coop
        self.next_step = next_step
        self.title = title
            
    def __repr__(self): return json.dumps(self.__dict__)


class SearchClan(ObjectState):
    name = "SEARCH_CLAN"
    def __init__(self, state):
        ObjectState.__init__(self, SearchClan.name, state)

    def cmd(state, option = SelectClanOption()) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": SearchClan.name, "input": state.current.last_option(), "result": None, "callback": None })


class InputFromMessage(ObjectState):
    name = "INPUT_FROM_MESSAGE"
    def __init__(self, state): 
        ObjectState.__init__(self, InputFromMessage.name, state)

    def cmd(state, result = None, option = None) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": InputFromMessage.name, "input": state.current.last_option(), "result": result })

    def __repr__(self): return json.dumps(self.__dict__)


class NewMatchOption:
    def __init__(self, clan1_id = None, next_step = None, match = None, title = ""):
        self.clan1_id = clan1_id
        self.next_step = next_step
        self.match = match
        self.title = title

    def __repr__(self): return json.dumps(self.__dict__)


class NewMatch(ObjectState):
    name = "NEW_MATCH"
    def __init__(self, state, next_step = None, match = None): 
        ObjectState.__init__(self, NewMatch.name, state)
        self.next_step = next_step
        self.match = match


    def cmd(state, option = NewMatchOption()) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": NewMatch.name, "input": state.current.last_option(), "result": None })


class SelectMap():
    name = "SELECT_MAP"
    def cmd(state, map = None, next_step = None) -> str:
        if next_step != None: state.current.next_step = next_step
        return json.dumps({ "action": SelectMap.name, "input": None, "result": map })


class MatchDate(ObjectState):
    name = "MATCH_DATE"
    def cmd(state, date = None, next_step = None) -> str:
        return json.dumps({ "action": MatchDate.name, "input": "CONFIRM", "result": date })


class MatchResult(ObjectState):
    name = "MATCH_RESULT"
    def __init__(self, state): 
        ObjectState.__init__(self, MatchResult.name, state)
        
    def cmd(state, caps1 = None, side1 = None, next_step = None) -> str:
        if next_step != None: state.current.next_step = next_step
        if caps1 == None or side1 == None:
            return json.dumps({ "action": MatchResult.name, "input": None, "result": side1 })    
        else:
            return json.dumps({ "action": MatchResult.name, "input": None, "result": { "caps1": caps1, "side1": side1 } })


class MatchConfirm(ObjectState):
    name = "MATCH_CONFIRM"
    def __init__(self, state): 
        ObjectState.__init__(self, MatchConfirm.name, state)

    def cmd(state, confirm = None, option = None) -> str:
        state.current.options.append(option)
        return json.dumps({ "action": MatchConfirm.name, "input": state.current.last_option(), "result": confirm })


class InputFromMessageOption:
    def __init__(self, field = None, title = ""):
        self.field = field
        self.title = title

    def __repr__(self): return json.dumps(self.__dict__)


class SelectFlagOption:
    def __init__(self, field = ""):
        self.field = field


class MatchConfirmOption:
    # def __init__(self, next_step = None, title = "", clan1 = None, coop1 = None, clan2 = None, coop2 = None, clan1_id = None, coop1_id = None, clan2_id = None, coop2_id = None, side1 = None, side2 = None, caps1 = None, caps2 = None, date = None, duration = None, map = None, factor = None, event = None, conf1 = None, conf2 = None):
    #     self.next_step = next_step
    #     self.title = title
    #     self.clan1 = clan1
    #     self.clan1_id = clan1_id
    #     self.coop1 = coop1
    #     self.coop1_id = coop1_id
    #     self.side1 = side1
    #     self.caps1 = caps1
    #     self.clan2 = clan2
    #     self.clan2_id = clan2_id
    #     self.coop2 = coop2
    #     self.coop2_id = coop2_id
    #     self.side2 = side2
    #     self.score2 = caps2
    #     self.date = date
    #     self.duration = duration
    #     self.map = map
    #     self.factor = factor
    #     self.event = event
    #     self.conf1 = conf1
    #     self.conf2 = conf2    
        
    def __init__(self, next_step = None, title = ""):
        self.next_step = next_step
        self.title = title
        
    def __repr__(self): return json.dumps(self.__dict__)
        

class Return(ObjectState):
    name = "RETURN"
    def __init__(self, state):
        super().__init__(Return.name, state)
        
    def cmd(state, result) -> str:
        return json.dumps({ "action": Return.name, "input": None, "result": result })

    async def process_message(state, cmd : SimpleNamespace):
        object_state = state.pop()
        
        logging.info(f"{cmd}")
        result = ReturnProcess.cmd(state.current.name, cmd.result)
        return result


class ReturnProcess(ObjectState):
    name = "RETURN_PROCESS"
    def cmd(action, result) -> str:
        return json.dumps({ "action": action, "input": None, "result": result })

