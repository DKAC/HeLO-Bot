import logging, time
from discord.embeds import Embed
from discord_components.component import Button
from database_models import *
from data import *
from object_models import *
from user_state import UserState
from env import * 


async def manage_clans(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = cmd.result )

    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != ManageClans.name:
        state.push(ManageClans(state))   
    
    
    embed = Embed(title = clans_title)
    
    components = [
        [            
            Button(emoji=emoji_new, custom_id = AddClan.cmd(state)),
            Button(emoji=emoji_edit, custom_id = EditClan.cmd(state)),
            Button(emoji=emoji_delete, custom_id = DeleteClan.cmd(state)),
        ], [            
            Button(emoji=emoji_home, custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    


async def edit_clan(state : UserState, cmd : SimpleNamespace):
    logging.info(f"{cmd}")
    error = None
    
    clans = Clans.get()
    
    if cmd.result == None:
        if cmd.action == EditClan.name:
            cmd = state.current.options[cmd.input]
            state.push(EditClan(state.current, cmd.next_step, clans_edit))
        else:           
            cmd = EditClanOption(next_step=EditClan.name)
            state.push(EditClan(state.current, cmd.next_step, clans_add))
            state.current.clan = Clan(f"local_{int(time.time())}") # id will be replaced when creating the clan via REST service
            
    else:       
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)

        if state.current.next_step == None: # first step: search for CLAN
            logging.info(f"CLAN: {result.selected}")    
            for clan in clans:
                if clan.id == result.selected:
                    state.current.clan = clan
                    state.current.next_step = EditClan.name
        
        elif result == "CONFIRM":
            if state.current.clan.id.startswith("local_"):
                Clans.create(state, state.current.clan)
            else:
                Clans.update(state, state.current.clan)
            return ManageClans.cmd(state)
        
        elif result.field == "SELECT_TAG":
            if result.input.lower() in [clan.tag.lower() for clan in clans]:
                error = clans_error_exists(result.input)
            else:
                state.current.clan.tag = result.input
            
        elif result.field == "SELECT_NAME":
            state.current.clan.name = result.input
            
        elif result.field == "SELECT_FLAG":
            state.current.clan.flag = result.flag
      
        elif result.field == "SELECT_INVITE":
            if result.input.startswith("https://discord.gg/"):
                state.current.clan.invite = result.input
            else:
                error = clans_error_invite(result.input)

    if state.current.next_step == None: # first step: search for CLAN
        return SearchClan.cmd(state, option = SearchClanOption(title = state.current.title))

    if state.current.next_step == "DONE":
        return ManageClans.cmd(state)
    
    description = clans_description(state.curent.clan)
    if error != None: description += f"\n\n{error}"
            
    embed = Embed(title = state.current.title, description = description)
    components = [
        [
            Button(emoji = emoji_tag, label = clans_tag, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_TAG", clans_tag_title))),
            Button(emoji = emoji_name, label = clans_name, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_NAME", clans_name_title))),
        ],
        [
            Button(emoji = emoji_flag, label = clans_flag, custom_id = SelectFlag.cmd(state, option = SelectFlagOption(field = "SELECT_FLAG"))),
            Button(emoji = emoji_link, label = clans_invite, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_INVITE", clans_invite_title))),
        ],
        [
            Button(emoji=emoji_ok, custom_id = EditClan.cmd(state, confirm = "CONFIRM")),
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
        

async def delete_clan(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result == None:
        cmd = state.current.options[cmd.input]
        state.push(DeleteClan(state, cmd.next_step))
    else:
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)
        
        if state.current.next_step == None: # first step: search for CLAN
            logging.info(f"CLAN: {result}")            
            state.current.clan = Clans.get(result.selected)
            state.current.next_step = "CONFIRM"

        elif state.current.next_step == "CONFIRM":
            logging.info(f"CONFIRM - delete from DB: {state.current.clan}")
            Clans.delete(state, state.current.clan.id)
            state.current.next_step = "DONE"

    if state.current.next_step == None: # first step: search for CLAN
        return SearchClan.cmd(state, option = SearchClanOption(title = "Delete Clan"))

    if state.current.next_step == "CONFIRM":     
        return DeleteClanConfirm.cmd(state, option = DeleteClanConfirmOption(clan = state.current.clan))
    
    if state.current.next_step == "DONE":  
        return ManageClans.cmd(state)
   
   
async def delete_clan_confirm(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "user": state.userid })
    
    state.push(DeleteClanConfirm(state.current))
    
    embed = Embed(title = clans_delete_confirm_title, description = clans_delete_confirm_description)
    
    components = [
        [
            Button(emoji='🆗', custom_id = DeleteClanConfirm.cmd(state, confirm = "CONFIRM" )),
            Button(emoji='🔼', custom_id = ManageClans.cmd(state))
        ]
    ]
    
    await state.current.respond(embed = embed, components = components)    