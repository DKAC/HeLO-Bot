import logging, time
from discord.embeds import Embed
from discord_components.component import Button
from database_models import *
from data import *
from object_models import *
from user_state import UserState
from env import * 


async def manage_events(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = cmd.result )

    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != ManageEvents.name:
        state.push(ManageEvents(state))   
    
    
    embed = Embed(title = events_title)
    
    components = [
        [            
            Button(emoji=emoji_new, custom_id = AddEvent.cmd(state)),
            Button(emoji=emoji_edit, custom_id = EditEvent.cmd(state)),
            Button(emoji=emoji_delete, custom_id = DeleteEvent.cmd(state)),
        ], [            
            Button(emoji=emoji_home, custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    


async def edit_event(state : UserState, cmd : SimpleNamespace):
    logging.info(f"{cmd}")
    error = None
    
    events = Events.get()
    
    if cmd.result == None:
        if cmd.action == EditEvent.name:
            cmd = state.current.options[cmd.input]
            state.push(EditEvent(state.current, cmd.next_step, events_edit))
        else:           
            cmd = EditEventOption(next_step=EditEvent.name)
            state.push(EditEvent(state.current, cmd.next_step, events_add))
            state.current.event = Event(f"local_{int(time.time())}") # id will be replaced when creating the event via REST service
            
    else:       
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)

        if state.current.next_step == None: # first step: search for event
            logging.info(f"event: {result.selected}")    
            for event in events:
                if event.id == result.selected:
                    state.current.event = event
                    state.current.next_step = EditEvent.name
        
        elif result == "CONFIRM":
            if state.current.event.id.startswith("local_"):
                Events.create(state, state.current.event)
            else:
                Events.update(state, state.current.event)
            return ManageEvents.cmd(state)
        
        elif result.field == "SELECT_TAG":
            if result.input.lower() in [event.tag.lower() for event in events]:
                error = events_error_exists(result.input)
            else:
                state.current.event.tag = result.input
            
        elif result.field == "SELECT_NAME":
            state.current.event.name = result.input
            
        elif result.field == "SELECT_EMOJI":
            state.current.event.emoji = result.input
      
        elif result.field == "SELECT_FACTOR":
            state.current.event.factor = result.factor
      
        elif result.field == "SELECT_INVITE":
            if result.input.startswith("https://discord.gg/"):
                state.current.event.invite = result.input
            else:
                error = events_error_invite(result.input)

    if state.current.next_step == None: # first step: search for event
        return SelectEvent.cmd(state) #, option = SearchEventOption(title = state.current.title))

    if state.current.next_step == "DONE":
        return ManageEvents.cmd(state)
    
    description = events_description(state.current.event)
    if error != None: description += f"\n\n{error}"
    embed = Embed(title = state.current.title, description = description)
    components = [
        [
            Button(emoji = emoji_tag, label = events_tag, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_TAG", events_tag_title))),
            Button(emoji = emoji_name, label = events_name, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_NAME", events_name_title))),
        ],
        [
            Button(emoji = emoji_emoji, label = events_emoji, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_EMOJI", events_emoji_title))),
            Button(emoji = emoji_factor, label = events_factor, custom_id = SelectFactor.cmd(state, option = SelectFlagOption(field = "SELECT_FACTOR"))),
            Button(emoji = emoji_link, label = events_invite, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_INVITE", events_invite_title))),
        ],
        [
            Button(emoji=emoji_ok, custom_id = EditEvent.cmd(state, confirm = "CONFIRM")),
            Button(emoji=emoji_home, custom_id = Home.cmd(state))
        ]
    ]
    
    if state.interaction != None:
        logging.info(f"responding to interaction: {embed.title} - {embed.description}")
        await state.interaction.respond(type = 7, content = "", embed = embed, components = components)
    else:
        logging.info(f"update message: {state.parent.interaction.message.id} ")
        await state.current.interaction.message.delete() # delete the message before the search
        await state.current.interaction.author.send(content = "", embed = embed, components = components)
        

async def delete_event(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result == None:
        cmd = state.current.options[cmd.input]
        state.push(DeleteEvent(state, cmd.next_step))
    else:
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)
        
        if state.current.next_step == None: # first step: search for event
            logging.info(f"event: {result}")            
            state.current.event = events.get(result.selected)
            state.current.next_step = "CONFIRM"

        elif state.current.next_step == "CONFIRM":
            logging.info(f"CONFIRM - delete from DB: {state.current.event}")
            events.delete(state, state.current.event.id)
            state.current.next_step = "DONE"

    if state.current.next_step == None: # first step: search for event
        return SelectEvent.cmd(state) #, option = SelectEventOption(title = "Delete event"))

    if state.current.next_step == "CONFIRM":     
        return DeleteEventConfirm.cmd(state, option = DeleteEventConfirmOption(event = state.current.event))
    
    if state.current.next_step == "DONE":  
        return ManageEvents.cmd(state)
   
   
async def delete_event_confirm(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "user": state.userid })
    
    state.push(DeleteEventConfirm(state.current))
    
    embed = Embed(title = events_delete_confirm_title, description = events_delete_confirm_description)
    
    components = [
        [
            Button(emoji='🆗', custom_id = DeleteEventConfirm.cmd(state, confirm = "CONFIRM" )),
            Button(emoji='🔼', custom_id = ManageEvents.cmd(state))
        ]
    ]
    
    await state.current.respond(embed = embed, components = components)    