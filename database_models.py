from datetime import datetime
import json, requests, os
from types import SimpleNamespace
import logging
from requests.models import Response


heloUrl = os.environ.get("HELO_URL")
   

########
# AUTH #
########
class Auth():
    
    def post(state):
        try:
            logging.info("-----------------------------------------")
            body = json.dumps({ "userid": state.userid, "pin": state.current.input })     

            Users.get(state, state.userid)
            response = requests.get(f"{heloUrl}/user/{state.userid}")
            user = SimpleNamespace(**json.loads(response.text))
            if hasattr(user, 'error'): # if user not found, create one
                logging.info(f"SIGNUP {state.userid}")
                response = requests.post(f"{heloUrl}/auth/signup", body, headers = state.headers)
                
            logging.info(f"LOGIN {state.userid}")
            response = requests.post(f"{heloUrl}/auth/login", body, headers = state.headers)
            jResponse = json.loads(response.content)
            
            if "error" in jResponse:
                logging.info("Authorization failed!")
                return None
                
            state.headers["Authorization"] = f"Bearer {jResponse['token']}"
            logging.info(f'{state.headers["Authorization"][:30]}...')
            logging.info("-----------------------------------------")
                    
            return requests.get(f"{heloUrl}/user/{state.userid}")
        except ConnectionError as ex:
            logging.error(f"Login error: {ex.__doc__}")
        except Exception as ex:
            logging.error(f"Login error: {ex}")

########
# USER #
########
class User():
    
    def __init__(self, id = None, userid = None, pin = None, name = None, role = None, clan = None, jUser = None):
        if jUser != None:
            self.id : str = jUser["_id"]["$oid"]
            self.userid : str = jUser["userid"]
            self.pin : str = jUser["pin"]
            self.name : str = jUser["name"]
            self.role : str = jUser["role"]
            self.clan : str = jUser["clan"]
        else:
            self.id : str = id
            self.userid : str = userid
            self.pin : str = pin
            self.name : str = name
            self.role : str = role
            self.clan : str = clan
    
class Users():

    def get(self, userid):
        try:
            logging.info(f"Users GET")
            jUser = json.loads(requests.get(f"{heloUrl}/user/{userid}").content)
            user = SimpleNamespace(**jUser)
            if hasattr(user, 'error'): 
                return None
            else:
                return User(jUser = jUser)
        except Exception as ex:
            logging.info(f"Error getting user data from DB: {ex}")

########
# CLAN #
########
class Clan():
    
    def __init__(self, id = "", tag = "", name = "", flag = "", invite = "", jClan = None):
        if jClan != None:
            self.id     : str = jClan["_id"]["$oid"]
            self.tag    : str = jClan["tag"]    if "tag" in jClan else ""
            self.name   : str = jClan["name"]   if "name" in jClan else ""
            self.flag   : str = jClan["flag"]   if "flag" in jClan else ""
            self.invite : str = jClan["invite"] if "invite" in jClan else ""
        else:
            self.id : str = id
            self.tag : str = tag
            self.name : str = name
            self.flag : str = flag
            self.invite : str = invite

    def __repr__(self): return json.dumps(self.__dict__)

    def to_json(self): return json.loads(json.dumps(self.__dict__)) # copy of dict
    
class Clans():
    
    def get(id = None):
        logging.info(f"Clans GET")
        try:
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
        except:
            logging.info(f"no clan found, id = {id}")
            return None
            
    def update(state, clan) -> Response:
        jClan = clan.to_json()
        jClan.pop("id")
        logging.info(f"Clan PUT {clan.id} {json.dumps(jClan)}")
        response = requests.put(f"{heloUrl}/clan/{clan.id}", json.dumps(jClan), headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, clan) -> Response:
        jClan = clan.to_json()        
        jClan.pop("id")
        logging.info(f"Clans POST {json.dumps(jClan)}")
        response = requests.post(f"{heloUrl}/clans", json.dumps(jClan), headers = state.headers)
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
    
    def to_json(self): return json.dumps({"tag": self.tag, "name": self.name, "flag": self.flag, "invite": self.invite})
               
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
        jEvent = event.to_json()
        logging.info(f"Event PUT {event.id} {jEvent}")
        response = requests.put(f"{heloUrl}/event/{event.id}", jEvent, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, event) -> Response:
        jEvent = event.to_json()
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
    
    def __init__(self, id = None, match_id = None, clan1_id = None, clan1 = None, coop1_id = None, coop1 = None, clan2_id = None, clan2 = None, coop2_id = None, coop2 = None, side1 = None, side2 = None, caps1 = None, caps2 = None, map = None, date = None, duration = None, factor = None, event = None, conf1 = None, conf2 = None, jMatch = None):
        if jMatch != None:
            self.id       : str = jMatch["_id"]["$oid"]
            self.match_id : str = jMatch["match_id"]
            self.clan1_id : str = jMatch["clan1_id"]
            self.clan1    : str = jMatch["clan1"]
            self.coop1_id : str = jMatch["coop1_id"] if "coop1_id" in jMatch else ""
            self.coop1    : str = jMatch["coop1"]    if "coop1"    in jMatch else ""
            self.clan2_id : str = jMatch["clan2_id"] 
            self.clan2    : str = jMatch["clan2"] 
            self.coop2_id : str = jMatch["coop2_id"] if "coop2_id" in jMatch else ""
            self.coop2    : str = jMatch["coop2"]    if "coop2"    in jMatch else ""
            self.side1    : str = jMatch["side1"]
            self.side2    : str = jMatch["side2"]
            self.caps1    : int = jMatch["caps1"]
            self.caps2    : int = jMatch["caps2"]
            self.map      : str = jMatch["map"]
            self.date     : str = datetime.fromtimestamp(jMatch["date"]["$date"]/1000).strftime("%Y-%m-%d")           
            self.duration : int = jMatch["duration"] if "duration" in jMatch else 90
            self.factor   : float = jMatch["factor"] if "factor" in jMatch else 0
            self.event    : str = jMatch["event"] if "event" in jMatch else ""
            self.conf1    : str = jMatch["conf1"] if "conf1" in jMatch else ""
            self.conf2    : str = jMatch["conf2"] if "conf2" in jMatch else ""
        else:
            self.id       : str = id      
            self.match_id : str = match_id
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
            self.conf1    : str = conf1   
            self.conf2    : str = conf2   
    
    def to_json(self): return json.dumps({
        "match_id": self.match_id, 
        "clan1_id": self.clan1_id, "clan1": self.clan1, "coop1_id": self.coop1_id, "coop1": self.coop1, 
        "clan2_id": self.clan2_id, "clan2": self.clan2, "coop2_id": self.coop2_id, "coop2": self.coop2, 
        "side1": self.side1, "side2": self.side2, "caps1": self.caps1, "caps2": self.caps2, "map": self.map, 
        "date": self.date, "duration": self.duration, "factor": self.factor, "event": self.event, 
        "conf1": self.conf1, "conf2": self.conf2,
    })
    
    def get_match_id(date, clan1, clan2):
        return f"{date}-{clan1}-{clan2}"

class Matches():
    
    def get(id = None, clan1_id = None, clan2_id = None):
        logging.info(f"Matches GET")
        if id != None:
            response = requests.get(f"{heloUrl}/match/{id}")
            jClan = json.loads(response.content) # get data from REST service
            match = Match(jMatch = jClan) # build object from json
            return match
        else:
            clan_args = []
            if clan1_id != None: clan_args.append(f"clan1_id={clan1_id}")
            if clan2_id != None: clan_args.append(f"clan2_id={clan2_id}")
            url_param = f'?{"&".join(clan_args)}' if len(clan_args) > 0 else ""
            response = requests.get(f"{heloUrl}/matches{url_param}")
            jMatches = json.loads(response.content) # get data from REST service
            matches = [Match(jMatch = jMatch) for jMatch in jMatches] # build objects from json
            return matches

    def update(state, match) -> Response:
        jMatch = match.to_json()
        logging.info(f"Matches PUT {match.id} {jMatch}")
        response = requests.put(f"{heloUrl}/match/{match.id}", jMatch, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, match) -> Response:
        jMatch = match.to_json()
        logging.info(f"Matches POST {jMatch}")
        response = requests.post(f"{heloUrl}/matches", jMatch, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Matches DELETE {id}")
        response = requests.delete(f"{heloUrl}/match/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response


class Score():
    
    def __init__(self, id = "", jScore = None):
        if jScore != None:
            self.id : str = jScore["_id"]["$oid"]
        else:
            self.id : str = id
    
    def to_json(self): return json.dumps({})

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
        jScore = score.to_json()
        logging.info(f"Scores PUT {score.id} {jScore}")
        response = requests.put(f"{heloUrl}/score/{score.id}", jScore, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def create(state, score) -> Response:
        jScore = score.to_json()
        logging.info(f"Scores POST {jScore}")
        response = requests.post(f"{heloUrl}/scores", jScore, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        logging.info(f"Scores DELETE {id}")
        response = requests.delete(f"{heloUrl}/score/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response