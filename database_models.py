import json, requests, os
from types import SimpleNamespace
import logging
from typing import List
from requests.models import Response
from user_state import get_state


heloUrl = os.environ.get("HELO_URL")

########
# AUTH #
########
class Auth():
    
    def post(state):
        logging.info("-----------------------------------------")
        # todo - check for non-empty pin
        # todo - on signup, set role to read-only
        body = json.dumps({ "userid": state.userid, "pin": state.current.input })     

        Users.get(state, state.userid)
        response = requests.get(f"{heloUrl}/user/{state.userid}")
        user = SimpleNamespace(**json.loads(response.text))
        if hasattr(user, 'error') is not None: # if user not found, create one
            logging.info(f"SIGNUP {state.userid}")
            response = requests.post(f"{heloUrl}/auth/signup", body, headers = state.headers)
            
        logging.info(f"LOGIN {state.userid}")
        response = requests.post(f"{heloUrl}/auth/login", body, headers = state.headers)
        state.headers["Authorization"] = f"Bearer {json.loads(response.content)['token']}"
        logging.info(f'{state.headers["Authorization"][:30]}...')
        logging.info("-----------------------------------------")
                
        return requests.get(f"{heloUrl}/user/{state.userid}")


########
# USER #
########
class User():
    
    def __init__(self, id = "", userid = "", pin = "", name = "", clan = "", jUser = None):
        if jUser != None:
            self.id : str = jUser["_id"]["$oid"]
            self.userid : str = jUser["userid"]
            self.pin : str = jUser["pin"]
            self.name : str = jUser["name"]
            self.clan : str = jUser["clan"]
        else:
            self.id : str = id
            self.userid : str = userid
            self.pin : str = pin
            self.name : str = name
            self.clan : str = clan
    
    def toJSON(self): return json.dumps({"userid": self.userid, "pin": self.pin, "name": self.name, "clan": self.clan})

class Users():

    def get(self, userid):
        logging.info(f"Users GET")
        jUser = requests.get(f"{heloUrl}/user/{userid}").content
        user = SimpleNamespace(**json.loads(jUser.text))
        if hasattr(user, 'error') is not None: 
            return None
        else:
            return User(jUser = jUser)


########
# CLAN #
########
class Clan():
    
    def __init__(self, id = "", tag = "", name = "", flag = "", invite = "", jClan = None):
        if jClan != None:
            self.id : str = jClan["_id"]["$oid"]
            self.tag : str = jClan["tag"]
            self.name : str = jClan["name"]
            self.flag : str = jClan["flag"]
            self.invite : str = jClan["invite"]
        else:
            self.id : str = id
            self.tag : str = tag
            self.name : str = name
            self.flag : str = flag
            self.invite : str = invite
    
    def toJSON(self): return json.dumps({"tag": self.tag, "name": self.name, "flag": self.flag, "invite": self.invite})
               
class Clans():
    
    def get(id = None):
        logging.info(f"Clans GET")
        if id == None:
            response = requests.get(f"{heloUrl}/clans")
            jClans = json.loads(response.content) # get data from REST service
            clans = [Clan(jClan = jClan) for jClan in jClans] # build objects from json
            return clans
        else:
            response = requests.get(f"{heloUrl}/clan/{id}")
            jClan = json.loads(response.content) # get data from REST service
            clan = Clan(jClan = jClan) # build object from json
            return clan
    
    def update(state, clan) -> Response:
        jClan = clan.toJSON()
        logging.info(f"Clan PUT {clan.id} {jClan}")
        response = requests.put(f"{heloUrl}/clan/{clan.id}", jClan, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, clan) -> Response:
        jClan = clan.toJSON()
        logging.info(f"Clans POST {jClan}")
        response = requests.post(f"{heloUrl}/clans", jClan, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Clans DELETE {id}")
        response = requests.delete(f"{heloUrl}/clan/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response


#########
# EVENT #
#########
class Event():
    
    def __init__(self, id = "", tag = "", name = "", flag = "", invite = "", jEvent = None):
        if jEvent != None:
            self.id : str = jEvent["_id"]["$oid"]
            self.tag : str = jEvent["tag"]
            self.name : str = jEvent["name"]
            self.flag : str = jEvent["flag"]
            self.invite : str = jEvent["invite"]
        else:
            self.id : str = id
            self.tag : str = tag
            self.name : str = name
            self.flag : str = flag
            self.invite : str = invite
    
    def toJSON(self): return json.dumps({"tag": self.tag, "name": self.name, "flag": self.flag, "invite": self.invite})
               
class Events():
    
    def get(id = None):
        logging.info(f"Events GET")
        if id == None:
            response = requests.get(f"{heloUrl}/events")
            jEvents = json.loads(response.content) # get data from REST service
            events = [Event(jEvent = jEvent) for jEvent in jEvents] # build objects from json
            return events
        else:
            response = requests.get(f"{heloUrl}/event/{id}")
            jEvent = json.loads(response.content) # get data from REST service
            event = Event(jEvent = jEvent) # build object from json
            return event
    
    def update(state, event) -> Response:
        jEvent = event.toJSON()
        logging.info(f"Event PUT {event.id} {jEvent}")
        response = requests.put(f"{heloUrl}/event/{event.id}", jEvent, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, event) -> Response:
        jEvent = event.toJSON()
        logging.info(f"Events POST {jEvent}")
        response = requests.post(f"{heloUrl}/events", jEvent, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Events DELETE {id}")
        response = requests.delete(f"{heloUrl}/event/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response

#########
# MATCH #
#########

class Match():
    
    def __init__(self, id = None, clan1_id = None, clan1 = None, coop1_id = None, coop1 = None, clan2_id = None, clan2 = None, coop2_id = None, coop2 = None, side1 = None, side2 = None, caps1 = None, caps2 = None, date = None, duration = None, factor = None, event = None, jMatch = None):
        if jMatch != None:
            self.id       : str = jMatch["_id"]["$oid"]
            self.clan1_id : str = jMatch["clan1_id"]
            self.clan1    : str = jMatch["clan1"]
            self.coop1_id : str = jMatch["coop1_id"]
            self.coop1    : str = jMatch["coop1"]
            self.clan2_id : str = jMatch["clan2_id"]
            self.clan2    : str = jMatch["clan2"]
            self.coop2_id : str = jMatch["coop2_id"]
            self.coop2    : str = jMatch["coop2"]
            self.side1    : str = jMatch["side1"]
            self.side2    : str = jMatch["side2"]
            self.caps1    : int = jMatch["caps1"]
            self.caps2    : int = jMatch["caps2"]
            self.map      : str = jMatch["map"]
            self.date     : str = jMatch["date"]
            self.duration : int = jMatch["duration"]
            self.factor   : str = jMatch["factor"]
            self.event    : str = jMatch["event"]
        else:
            self.id       : str = id      
            self.clan1_id : str = clan1_id
            self.clan1    : str = clan1   
            self.coop1_id : str = coop1_id
            self.coop1    : str = coop1   
            self.clan2_id : str = clan2_id
            self.clan2    : str = clan2   
            self.coop2_id : str = coop2_id
            self.coop2    : str = coop2   
            self.side1    : str = side1   
            self.side2    : str = side2   
            self.caps1    : int = caps1   
            self.caps2    : int = caps2   
            self.map      : str = map     
            self.date     : str = date    
            self.duration : int = duration
            self.factor   : str = factor    
            self.event    : str = event   
    
    def toJSON(self): return json.dumps({
        "clan1_id": self.clan1_id, "clan1": self.clan1, "coop1_id": self.coop1_id, "coop1": self.coop1, 
        "clan2_id": self.clan2_id, "clan2": self.clan2, "coop2_id": self.coop2_id, "coop2": self.coop2, 
        "side1": self.side1, "side2": self.side2, "caps1": self.caps1, "caps2": self.caps2, "map": self.map, 
        "date": self.date, "duration": self.duration, "factor": self.factor, "event": self.event, 
    })

class Matches():
    
    def get(id = None):
        logging.info(f"Matches GET")
        if id == None:
            response = requests.get(f"{heloUrl}/matches")
            jMatches = json.loads(response.content) # get data from REST service
            clans = [Match(jMatch = jMatch) for jMatch in jMatches] # build objects from json
            return clans
        else:
            response = requests.get(f"{heloUrl}/match/{id}")
            jClan = json.loads(response.content) # get data from REST service
            clan = Match(jMatch = jClan) # build object from json
            return clan

    def update(state, match) -> Response:
        jMatch = match.toJSON()
        logging.info(f"Matches PUT {match.id} {jMatch}")
        response = requests.put(f"{heloUrl}/match/{match.id}", jMatch, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, clan) -> Response:
        jMatch = clan.toJSON()
        logging.info(f"Matches POST {jMatch}")
        response = requests.post(f"{heloUrl}/matches", jMatch, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Matches DELETE {id}")
        response = requests.delete(f"{heloUrl}/match/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response


class Scores():
    
    def get(id = None):
        logging.info(f"Scores GET")
        if id == None:
            response = requests.get(f"{heloUrl}/scores")
            jScores = json.loads(response.content) # get data from REST service
            scores = [Score(jScore = jScore) for jScore in jScores] # build objects from json
            return scores
        else:
            response = requests.get(f"{heloUrl}/score/{id}")
            jScore = json.loads(response.content) # get data from REST service
            score = Score(jScore = jScore) # build object from json
            return score

    def update(state, score) -> Response:
        jScore = score.toJSON()
        logging.info(f"Scores PUT {score.id} {jScore}")
        response = requests.put(f"{heloUrl}/score/{score.id}", jScore, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, score) -> Response:
        jScore = score.toJSON()
        logging.info(f"Scores POST {jScore}")
        response = requests.post(f"{heloUrl}/scores", jScore, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Scores DELETE {id}")
        response = requests.delete(f"{heloUrl}/score/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response