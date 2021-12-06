#########################################################################################
# state objects to hold the state of the current and previous steps                     #
# option objects to hold the parameters when executing the next step                    #
#########################################################################################

class ObjectState:
    name = None
    def __init__(self, name, state, action = None):
        self.interaction = state.interaction
        self.message = state.message
        self.options = []
        self.input = ""
        self.name = name
        self.action = action
        
    def __repr__(self): return f"{self.name}(input = {self.input}, options = {self.options})"
      
    def last_option(self):
        return len(self.options) - 1

    async def respond(self, content = "", embed = None, components = None):
        await self.interaction.respond(type = 7, content = content, embed = embed, components = components)

