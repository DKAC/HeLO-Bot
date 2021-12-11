#########################################################################################
# state objects to hold the state of the current and previous steps                     #
# option objects to hold the parameters when executing the next step                    #
#########################################################################################
  
    
from discord.errors import NotFound


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
            await self.interaction.respond(type = 7, content = content, embed = embed, components = components)
        except NotFound as ex:
            await self.interaction.message.delete()
            await self.message.channel.send(embed = embed, components = components)
