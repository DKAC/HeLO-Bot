from object_models import *
from pages.login import login
from pages.home import home
from pages.match_duration import match_duration
from pages.match_players import match_players
from pages.select_clan import select_clan
from pages.search_clan import search_clan, search_clan_callback
from pages.manage_clans import manage_clans, edit_clan, delete_clan, delete_clan_confirm
from pages.new_match import new_match
from pages.match_result import match_result
from pages.match_date import match_date
from pages.select_event import select_event
from pages.select_map import select_map
from pages.select_flag import select_flag
from pages.match_confirm import match_confirm
from pages.input_from_message import input_from_message, input_from_message_callback

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
    NewMatch.name:          new_match,
    MatchResult.name:       match_result,
    MatchDuration.name:     match_duration,
    MatchPlayers.name:      match_players,
    MatchDate.name:         match_date,
    SelectMap.name:         select_map,
    SelectEvent.name:       select_event,
    SelectFlag.name:        select_flag,
    MatchConfirm.name:      match_confirm,
    InputFromMessage.name:  input_from_message,
    Return.name:            Return.process_message
}
async def other_action(state, args): 
    logging.info(f"action not recognised: {state.interaction.custom_id}")
    await state.current.respond()

callbacks = {
    SearchClan.name:        search_clan_callback,
    InputFromMessage.name:  input_from_message_callback,
}