#!/usr/bin/python3
#
# busybee-bot
#
# A Discord bot which watches users activity status.
# If activity changes to streaming it adds a role to the user and removes it
# when the streaming activity stops
# Uses discord.py (https://discordpy.readthedocs.io/) for interacting with discord servers
#
# This is free and unencumbered software released into the public domain.
# For more information, please refer to <https://unlicense.org>

import os
import traceback
import discord
from discord import ActivityType
from datetime import datetime

####################################################################
# Bot Settings:
# discord bot token; found in the discord developer portal after creating the bot
TOKEN = "discord-bot-token"
# the role users should be added to while streaming
ROLE = "role-name"
# discord users to ignore; this is a python list ie ["user1", "user2"]
# useful to ignore bots which always have streaming activity active
blacklist = [""]
# log messages to file
enable_logging = True
# log debugging messages and enable debug output
enable_debugging = False
# logfile location
logfile_name = os.path.dirname(os.path.realpath(__file__)) + "/busybee-bot.py.log"
# End of Settings
####################################################################

# instantiate the discord client (will not run yet)
client = discord.Client()

# when bot comes online "on_ready" event handler will be called
@client.event
async def on_ready():
    _l("logged in as {0.user}".format(client))

# this event fires whenever something changes for a user
@client.event
async def on_member_update(before, after):
    try:
        full_username = "{0}#{1}".format(after.name, after.discriminator)
        _ld("Got member_update for %s" %(full_username))

        if full_username in blacklist:
            _ld("Ignoring user %s: is on blacklist" %(full_username))
            return

        if not activity_is_changed(before, after):
            return

        new_role = get_role_object(client, ROLE)
        if type(after.activities) is not tuple:
            _ld("after.activities was not a tuple")
            _l("Removing role \"{0}\" from user \"{1}\" (1)".format(ROLE, full_username))
            await after.remove_roles(new_role)
            return


        if not len(after.activities):
            _ld("length of after.activities is 0")
            _l("Removing role \"{0}\" from user \"{1}\"".format(ROLE, full_username))
            await after.remove_roles(new_role)
            return

        stream = None

        # find the streaming activity
        for activity in after.activities:
            _ld("type of acitivity: {0}".format(activity.type))
            if activity.type == ActivityType.streaming:
                _ld("found streaming")
                stream = activity
                break
        if stream == None:
            # if no activity.type was streaming, remove role
            _ld("No ActivityType.streaming in Activity types")
            _l("Removing role \"{0}\" from user \"{1}\"".format(ROLE, full_username))
            await after.remove_roles(new_role)
            return

        # activity type is streaming, so add role
        _ld("Platform: {0.platform}; Game: {0.game}; Url: {0.url}; Type: {0.type};".format(stream))
        if stream.twitch_name:
            _ld(" Twitchname: {0}".format(stream.twitch_name))

        _l("Adding role \"{0}\" to user \"{1}\"".format(ROLE, full_username))
        await after.add_roles(new_role)

    except:
        _l("Caught unknown exception in on_member_update")
        _l(traceback.format_exc())


# returns the role object corresponding to rolename
def get_role_object(client, rolename):
    roles = client.guilds[0].roles
    for r in roles:
        if r.name == rolename:
            _ld("Found requested role: {0}".format(r.id))
            return r

# compares before and after Member objects's activities
def activity_is_changed(before, after):
    status_b = False
    status_a = False

    # see if there are valid activities in Member objects
    if type(before.activities) is tuple and len(before.activities):
        status_b = True # acitivity was set before

    if type(after.activities) is tuple and len(after.activities):
        status_a = True # acitivity is set now

    if status_a == status_b:
        if before.activities == after.activities:
            _ld("Activity status unchanged")
            return False # no change

    _ld("before activities: {}".format(before.activities))
    _ld("after activities:  {}".format(after.activities))

    # before and after differ
    _ld("Activity status has changed")
    return True

 # Logging to file and/or STDOUT
def _l(text, debug = False):
    now = datetime.now()
    logstring = "[%s] %s" %(now, text)

    if enable_debugging:
        print(logstring)

    if not enable_logging:
        return

    if not debug or enable_debugging:
        if logfile_name:
            f = open(logfile_name, "a")
        else:
            f = open("fronkbot.log", "a")
        f.write("{}\n".format(logstring))
        f.close()

# short-hand function for debug logging
def _ld(text):
    _l(text, True)

# run discord client
client.run(TOKEN)
