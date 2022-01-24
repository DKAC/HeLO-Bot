import logging, os, pytz, discord
from discord_components.client import DiscordComponents
from datetime import date, timedelta

from object_state import not_empty

discord_token = os.environ.get("DISCORD_TOKEN")
matches_channel = os.environ.get("MATCHES_CHANNEL")
scores_channel = os.environ.get("SCORES_CHANNEL")
heloUrl = os.environ.get("HELO_URL")

tz = pytz.timezone("Europe/Berlin")

logging.basicConfig(encoding='utf-8', level=logging.INFO, format=f"%(filename)20s:%(lineno)-3s - %(funcName)-30s %(message)s")
logging.getLogger("discord").setLevel(logging.ERROR)

discordClient = discord.Client()
DiscordComponents(discordClient)

emoji_side = { "Allies": "<:Allies:921762173590581299>", "Axis": "<:Axis:921762520899924050>" }
emoji_number = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:"]

emoji_status_not_confirmed = "❓"
emoji_status_confirmed = "☑️"
emoji_status_released = "✅"
emoji_status_other = "🤼"
emoji_clan = "🚹"
emoji_coop = "🚻"
emoji_clan_admin = "🚼"
emoji_data = "🗄️"
emoji_home = "🔼"
emoji_back = "◀️"
emoji_ok = "🆗"
emoji_zero = "0️⃣"
emoji_one = "1️⃣"
emoji_two = "2️⃣"
emoji_three = "3️⃣"
emoji_four = "4️⃣"
emoji_five = "5️⃣"
emoji_six = "6️⃣"
emoji_seven = "7️⃣"
emoji_eight = "8️⃣"
emoji_nine = "9️⃣"
emoji_login = "🔑"
emoji_new = "🆕"
emoji_edit = "✏️"
emoji_delete = "🗑️"
emoji_tag = "🏷️"
emoji_name = "📛"
emoji_flag = "🏳️‍🌈"
emoji_link = "🔗"
emoji_role = "🗝️"
emoji_players = "👨‍👨‍👦‍👦"
emoji_event = "🎖️"
emoji_date = "🗓️"
emoji_map = "🗺️" 
emoji_score = '5️⃣'
emoji_duration = '⏱️'
emoji_confirm_admin = '🅾️'
emoji_factor = '✖️'
emoji_emoji = '😉'


#### LOGIN ####
login_title = "Login"
login_description = "Enter your PIN"
login_failed = "❌    Login failed    ❌"
logout_title = "Done"
logout_description = "logged out"
logout_login = "Login"

#### HOME ####
home_title = "HeLO - Hell Let Loose ELO"

def home_description(state): return "\n".join([
        f"User: {state.user.name} ({state.user.role})",
        f"Clan: {state.clan.flag} {state.clan.tag}" if state.clan != None else None,
        f"",
        f"**__Legend__** (up to 5 matches, up to 2 weeks)",
        f"{emoji_status_not_confirmed} waiting for confirmation",
        f"{emoji_status_confirmed} waiting for opponent confirmation",
        f"{emoji_status_released} confirmed by both parties (or admin)",
    ])

def home_match_status(match): return f"{match.date} {match.clan1} vs. {match.clan2}"

home_new_match = "new match"
home_new_coop_match = "new coop match"
home_new_match_admin = "new match (admin)"
home_search_match_admin = "search match (admin)"
home_clans = "clans"
home_users = "users"
home_events = "events"
home_logout = "logout"


#### match confirm ####
match_confirm_title = "Match confirmation"
match_confirm_vs = 'vs.'
match_confirm_clan1_title = "Change 1. Clan"
match_confirm_coop1_title = "Change 1. Coop"
match_confirm_clan2_title = "Change 2. Clan"
match_confirm_coop2_title = "Change 1. Coop"

def match_confirm_description(match_description): return "{match_description}**Confirm match (your user id will be added to the match data)**"


#### match date ####
match_date_title = "Match date"

def match_date_description(match_description): return f"{match_description}**Select match date**"
def match_date(days): return date.today() - timedelta(days = days)
def match_date_label(days): return "today" if days == 0 else "yesterday" if days == 1 else match_date(days).strftime('%d %b')
def match_date_iso(days): return match_date(days).isoformat()


#### match duration ####
match_duration_title = "Match duration"

def match_duration_description(match_description): return f"{match_description}**Select match duration**"


#### match players ####
match_players_title = "Match players"

def match_players_description(match_description): return f"{match_description}**Select match players**"


#### match result ####
match_result_title = "Match result"

def match_result_description(match_description): return f"{match_description}**Select match result and side below**"


#### input from message ####
input_from_message_description = "Enter value as message text below:"


#### CLANS ####
clans_title = "Manage Clans"
clans_edit = "Edit Clan"
clans_add = "Add Clan"
clans_tag = "tag"
clans_flag = "flag"
clans_invite = "invite"
clans_name = "name"
clans_tag_title = "Enter Clan Tag"
clans_name_title = "Enter Clan Name"
clans_invite_title = "Enter Disord Invite URL"
clans_delete_confirm_title = "Confirm clan deletion"
clans_delete_confirm_description = "**Are you absolutely sure, this clan should be deleted?**"

def clans_error_exists(input): return f"***Invalid input: clan with tag '{input}' already exists***"
def clans_error_invite(input): return f"***Invalid input: discord invites have the form 'https://discord.gg/??????????'***"

def clans_description(clan): return "\n".join([
        f"Tag: {clan.tag}",
        f"Name: {clan.name}",
        f"Emoji: {clan.emoji}",
        f"Invite: {clan.invite}"
    ])


#### EVENTS ####
events_title = "Manage Event"
events_edit = "Edit Event"
events_add = "Add Event"
events_tag = "tag"
events_flag = "flag"
events_factor = "factor"
events_emoji = "emoji"
events_invite = "invite"
events_name = "name"
events_tag_title = "Enter Event Tag"
events_name_title = "Enter Event Name"
events_emoji_title = "Enter Emoji"
events_invite_title = "Enter Disord Invite URL"
events_delete_confirm_title = "Confirm event deletion"
events_delete_confirm_description = "**Are you absolutely sure, this event should be deleted?**"

def events_error_exists(input): return f"***Invalid input: event with tag '{input}' already exists***"
def events_error_invite(input): return f"***Invalid input: discord invites have the form 'https://discord.gg/??????????'***"

def events_description(event): return "\n".join([
        f"Tag: {event.tag}",
        f"Name: {event.name}",
        f"Emoji: {event.emoji}",
        f"Factor: {event.factor}",
        f"Invite: {event.invite}"
    ])


#### USERS ####
users_title = "Manage Users"
users_edit = "Edit User"
users_add = "Add User"
users_userid = "user"
users_name = "name"
users_clan = "clan"
users_role = "role"
users_userid_title = "Enter User ID (discord)"
users_name_title = "Enter User Name"
users_delete_title = "Delete User"
users_delete_confirm_title = "Confirm user deletion"
users_delete_confirm_description = "**Are you absolutely sure, this user should be deleted?**"

def users_description(user, clan): return "\n".join([
        f"User ID: {user.userid}",
        f"Name: {user.name}",
        f"Clan: {clan.tag}" if clan != None else f"Clan: {user.clan}",
        f"Role: {user.role}"
    ])


#### MATCH MESSAGE DESCRIPTION ####

def match_message_description(event, clan1, coop1, clan2, coop2, match, map): 
    s = f"{event['emoji']} **{event['name']}** {event['emoji']}\n" if not_empty(event) else ""
    s += f"{clan1.flag} "   if not_empty(clan1.flag)  else ""
    s += f"{clan1.tag}"
    s += " & "              if not_empty(match.coop1) else ""
    s += f"{coop1.flag} "   if not_empty(coop1.flag)  else ""
    s += f"{coop1.tag}"     if not_empty(match.coop1) else ""
    s += " vs. "
    s += f"{clan2.flag} "   if not_empty(clan2.flag)  else ""
    s += f"{clan2.tag}"
    s += " & "              if not_empty(match.coop2) else ""
    s += f"{coop2.flag} "   if not_empty(coop2.flag)  else ""
    s += f"{coop2.tag}"     if not_empty(match.coop2) else ""
    s += "\n"
    s += f":calendar_spiral: {match.date}" if match.date != None else "???"
    s += "\n"
    s += f"{emoji_players} {match.players} vs. {match.players}" if not_empty(match.players) else "???"
    s += "\n"
    s += f":map: {map['name']}" if not_empty(map) else "???"
    s += "\n"
    s += emoji_side[match.side1] if not_empty(match.side1) else "???"
    s += "  "
    s += emoji_number[match.caps1] if match.caps1 != None else "?"
    s += " : "
    s += emoji_number[match.caps2] if match.caps2 != None else "?"
    s += "  "
    s += emoji_side[match.side2] if not_empty(match.side2) else "???"
    s += f" - :stopwatch: {match.duration} min" if not_empty(match.duration) else " - ??? min"
    s += "\n\n"
    return s    