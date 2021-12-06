import json, requests, os
from types import SimpleNamespace
import logging
from typing import List
from requests.models import Response
from user_state import get_state


heloUrl = os.environ.get("HELO_URL")


class Auth():
    
    def post(state):
        logging.info("-----------------------------------------")
        # todo - check for non-empty pin
        # todo - on signup, set role to read-only
        body = json.dumps({ "userid": state.userid, "pin": state.current.input })     

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
    
    def get(id = None) -> List[Clan]:
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
        print(requests.get(f"{heloUrl}/clan/{id}"))
        return response
        
    def create(state, clan) -> Response:
        jClan = clan.toJSON()
        logging.info(f"Clans POST {jClan}")
        response = requests.post(f"{heloUrl}/clans", jClan, headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response
        
    def delete(state, id):
        print(f"DELETE {id}")
        response = requests.delete(f"{heloUrl}/clan/{id}", headers = state.headers)
        logging.info(f"HTTP {response.status_code} {response.text}")
        return response