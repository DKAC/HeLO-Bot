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
#            if content == "" and embed == None and components == None: 
            await self.interaction.respond(type = 7, content = content, embed = embed, components = components)
            # else:
            #     logging.info(f"{self.interaction.message.id}")
            #     logging.info(f"{self.interaction.message.channel.id}")
            #     channel = self.interaction.message.channel
            #     await self.interaction.message.delete()
            #     await channel.send(content = content + ".", embed = embed, components = components)
            
        except NotFound as ex:
            await self.interaction.message.delete()
            if self.message != None:
                await self.message.channel.send(content = content, embed = embed, components = components)
            else:
                logging.warning("todo")
                # todo - send message by user id
        except Exception as ex:
            logging.error(f"exception: {ex}")
