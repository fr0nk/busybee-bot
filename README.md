busybee-bot
===========

A Discord bot which watches users activity status.
If activity changes to streaming it adds a role to the user and removes it
when the streaming activity stops

Uses discord.py (https://discordpy.readthedocs.io/) for interacting with discord servers

### License

This is free and unencumbered software released into the public domain.
For more information, please refer to <https://unlicense.org>

### Requirements

Depends on python3 and discord.py.
On Ubuntu install discord.py with `pip3 -U discord.py`

### Discord Bot Setup

* Go to your Discord Developer Portal (https://discordapp.com/developers/applications)
* Create new application
* Get Client ID from "General Information" page (will be needed later)
* Create Bot on "Bot" page
* Get Token from the "Bot" page (will be needed later)
* Open invite Link to invite the bot into your Discord Server (replace {client_id} with your bots client id):
`https://discordapp.com/oauth2/authorize?&client_id={client_id}&scope=bot&permissions=268435456`

 This will add the bot to your server and create a new role for the bot itself. Permissions 268435456 grants the "Manage Roles" Permission

* In your Discord Server Settings drag the new bot role above the role that it's supposed to add the streamers to
* Open busybee-bot.py
* Change TOKEN to the bot token copied earlier
* Change ROLE to the role streamers should be added to
