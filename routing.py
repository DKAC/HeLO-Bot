from object_models import *
from pages.login import login
from pages.home import home
from pages.manage_events import delete_event, delete_event_confirm,  edit_event, manage_events
from pages.match_duration import match_duration
from pages.match_players import match_players
from pages.select_clan import select_clan
from pages.search_clan import search_clan, search_clan_callback
from pages.search_user import search_user, search_user_callback
from pages.search_match import search_match, search_match_callback
from pages.manage_clans import manage_clans, edit_clan, delete_clan, delete_clan_confirm
from pages.manage_users import manage_users, edit_user, delete_user, delete_user_confirm
from pages.new_match import new_match
from pages.match_result import match_result
from pages.match_date import match_date
from pages.select_event import select_event
from pages.select_map import select_map
from pages.select_flag import select_flag
from pages.select_factor import select_factor
from pages.match_confirm import match_confirm
from pages.input_from_message import input_from_message, input_from_message_callback
from pages.select_role import select_role
from pages.select_user import select_user

actions = { 
    Login.name:             login,
    Home.name:              home,
    SelectClan.name:        select_clan,
    SearchClan.name:        search_clan,
    ManageClans.name:       manage_clans,
    AddClan.name:           edit_clan,
    EditClan.name:          edit_clan,
    DeleteClan.name:        delete_clan,
    DeleteClanConfirm.name: delete_clan_confirm,
    ManageEvents.name:      manage_events,
    AddEvent.name:          edit_event,
    EditEvent.name:         edit_event,
    DeleteEvent.name:       delete_event,
    DeleteEventConfirm.name:delete_event_confirm,
    SelectUser.name:        select_user,
    SearchUser.name:        search_user,
    ManageUsers.name:       manage_users,
    AddUser.name:           edit_user,
    EditUser.name:          edit_user,
    DeleteUser.name:        delete_user,
    DeleteUserConfirm.name: delete_user_confirm,
    NewMatch.name:          new_match,
    SearchMatch.name:       search_match,
    MatchResult.name:       match_result,
    MatchDuration.name:     match_duration,
    MatchPlayers.name:      match_players,
    MatchDate.name:         match_date,
    SelectMap.name:         select_map,
    SelectEvent.name:       select_event,
    SelectFlag.name:        select_flag,
    SelectFactor.name:      select_factor,
    MatchConfirm.name:      match_confirm,
    InputFromMessage.name:  input_from_message,
    SelectRole.name:        select_role,
    Return.name:            Return.process_message
}
async def other_action(state, args): 
    logging.info(f"action not recognised: {state.interaction.custom_id}")
    await state.current.respond()

callbacks = {
    SearchClan.name:        search_clan_callback,
    SearchUser.name:        search_user_callback,
    SearchMatch.name:       search_match_callback,
    InputFromMessage.name:  input_from_message_callback,
}