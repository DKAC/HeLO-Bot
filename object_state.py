#########################################################################################
# state objects to hold the state of the current and previous steps                     #
# option objects to hold the parameters when executing the next step                    #
#########################################################################################
  
    
import logging
from discord.errors import NotFound


def not_empty(s): return s != None and s != ""
def empty(s): return s == None or s == ""


class ObjectState():
    name = None
    def __init__(self, name, state, action = None):
        self.interaction = state.interaction
        self.message = state.message
        self.options = []
        self.input = ""
        self.title = None
        self.name = name
        self.action = action
              
    def last_option(self):
        return len(self.options) - 1

    async def respond(self, content = "", embed = None, components = None):
        try:
            if content == "" and embed == None and components == None:
                await self.interaction.respond(type = 7, content = content, embed = embed, components = components)
            else:            
                logging.info(f"send response: {self.interaction.message.id}")
                channel = self.interaction.message.channel
                await channel.send(content = content, embed = embed, components = components)
                await self.interaction.message.delete()
            
        except Exception as ex:
            try:
                logging.warning("????????????????????????? todo ?????????????????????????")
            except Exception as ex:
                logging.error(f"exception: {ex}")
