import logging, time
from discord.embeds import Embed
from discord_components.component import Button
from database_models import *
from data import *
from object_models import *
from user_state import UserState
from env import *


async def manage_users(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = cmd.result )

    states = state.pop_to(Home)
    logging.info(f"states = {states}")
    if state.current.name != ManageUsers.name:
        state.push(ManageUsers(state))   
    
    
    embed = Embed(title = users_title)
    
    components = [
        [            
            Button(emoji="🆕", custom_id = AddUser.cmd(state)),
            Button(emoji="✏️", custom_id = EditUser.cmd(state)),
            Button(emoji="🗑️", custom_id = DeleteUser.cmd(state)),
        ], [            
            Button(emoji='🔼', custom_id = Home.cmd(state))
        ]        
    ]
    
    await state.current.respond(embed = embed, components = components)    


async def edit_user(state : UserState, cmd : SimpleNamespace):
    logging.info(f"{cmd}")
    error = None
       
    if cmd.result == None:
        if cmd.action == EditUser.name:
            cmd = state.current.options[cmd.input]
            state.push(EditUser(state.current, cmd.next_step, users_edit))
        else:           
            cmd = EditUserOption(next_step=EditUser.name)
            state.push(EditUser(state.current, cmd.next_step, users_add))
            state.current.user = User(f"local_{int(time.time())}") # id will be replaced when creating the user via REST service
            
    else:       
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)

        if state.current.next_step == None: # first step: search for USER
            logging.info(f"USER: {result.userid}")
            user = Users.get(userid=result.userid)
            state.current.user = user
            state.current.next_step = EditUser.name
        
        elif result == "CONFIRM":
            if state.current.user.id.startswith("local_"):
                Users.create(state, state.current.user)
            else:
                Users.update(state, state.current.user)
            return ManageUsers.cmd(state)
        
        elif hasattr(result, "selected"):
            state.current.user.clan = result.selected
      
        elif hasattr(result, "role"):
            state.current.user.role = result.role

        elif result.field == "SELECT_USERID":
            state.current.user.userid = result.input
            
        elif result.field == "SELECT_NAME":
            state.current.user.name = result.input
            
    if state.current.next_step == None: # first step: search for USER
        return SearchUser.cmd(state, option = SearchUserOption(title = state.current.title))

    if state.current.next_step == "DONE":
        return ManageUsers.cmd(state)
    
    clan = Clans.get(state.current.user.clan) if state.current.user.clan != None else None
    
    description = users_description(state.current.user, clan)
    if error != None: description += f"\n\n{error}"
            
    embed = Embed(title = state.current.title, description = description)
    components = [
        [
            Button(emoji = emoji_tag, label = users_userid, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_USERID", users_userid_title))),
            Button(emoji = emoji_name, label = users_name, custom_id = InputFromMessage.cmd(state, option = InputFromMessageOption("SELECT_NAME", users_name_title))),
            Button(emoji = emoji_clan, label = users_clan, custom_id = SearchClan.cmd(state)),
            Button(emoji = emoji_role, label = users_role, custom_id = SelectRole.cmd(state)),
        ],
        [
            Button(emoji=emoji_ok, custom_id = EditUser.cmd(state, confirm = "CONFIRM")),
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
        

async def delete_user(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")
    
    if cmd.result == None:
        cmd = state.current.options[cmd.input]
        state.push(DeleteUser(state, cmd.next_step))
    else:
        result = cmd.result if type(cmd.result) == str else SimpleNamespace(**cmd.result)
        
        if state.current.next_step == None: # first step: search for USER
            logging.info(f"USER: {result}")            
            state.current.user = Users.get(result.userid)
            state.current.next_step = "CONFIRM"

        elif state.current.next_step == "CONFIRM":
            logging.info(f"CONFIRM - delete from DB: {state.current.user}")
            Users.delete(state, state.current.user.userid)
            state.current.next_step = "DONE"

    if state.current.next_step == None: # first step: search for USER
        return SearchUser.cmd(state, option = SearchUserOption(title = users_delete_title))

    if state.current.next_step == "CONFIRM":     
        return DeleteUserConfirm.cmd(state, option = DeleteUserConfirmOption(user = state.current.user))
    
    if state.current.next_step == "DONE":  
        return ManageUsers.cmd(state)
   
   
async def delete_user_confirm(state, cmd : SimpleNamespace):
    logging.info(f"{cmd}")    
    
    if cmd.result != None:
        return Return.cmd(state, result = { "user": state.userid })
    
    state.push(DeleteUserConfirm(state.current))
    
    embed = Embed(title = users_delete_confirm_title, description = users_delete_confirm_description)
    
    components = [
        [
            Button(emoji='🆗', custom_id = DeleteUserConfirm.cmd(state, confirm = "CONFIRM" )),
            Button(emoji='🔼', custom_id = ManageUsers.cmd(state))
        ]
    ]
    
    await state.current.respond(embed = embed, components = components)    