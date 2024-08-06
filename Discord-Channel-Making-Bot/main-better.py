########################################################################################################################
# This is a very basic discord bot that is meant to be used in smaller servers
# All it really does is create a new voice channel when the user joins a specific voice channel
# It sets the new channel name when it is created.
# The channel will be deleted once all user's leave the channel, or it is manually destroyed by an admin.
# This is really simple and works ok. I just wanted something to make vcs on my buddy's server.


# Created on 8/5/2024
# Created by Domo The Slime
########################################################################################################################

# Imports discord lib for usage
import discord
from discord.ext import commands

# Sets the intents for the bot
# Pretty much the permissions on this side
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.voice_states = True

# Creates the bot instance to control some of our events
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary used to hold the user ids related to the voice channel
user_channels = {}

TARGET_VC_CHANNEL = 000000000

# Basic event tracker for bot to show it was logged in correctly
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


########################################################################################################################
# Member in the function arguments represents the user to track whether they join or leave
# Before represents the state of the user before the update occurs
# After represents the state of the user after the update occurs
########################################################################################################################


# Main event code
# Tracks user movement into channels and creates/deletes channels on certain conditions
@bot.event
async def on_voice_state_update(member, before, after):

    # Essentially gets the server which we will use later
    guild = member.guild
    # Gets the server category/branch where we want the voice channels to be made
    category = discord.utils.get(guild.categories, name='User VCs')

    # If the user joined the target voice channel, then this branch will run
    if after.channel and after.channel.id == TARGET_VC_CHANNEL:

        # If the member (person who joined channel) has not made a voice channel yet, then a new channel will be made
        if member.id not in user_channels:
            # Gets the user's name
            username = member.name

            # Sets the channel name for the made VC
            channel_name = f'{username}\'s VC'

            # Creates the new channel by calling the create_voice_channel command with the channel name and category
            new_channel = await guild.create_voice_channel(channel_name, category=category)

            # Adds the user who created the channel to the user_channels dict
            user_channels[member.id] = new_channel.id

            # Moves the user into the newly created channel via the move_to command
            await member.move_to(new_channel)  # Move the user to the new channel
            print(f'Created and moved user to new voice channel: {new_channel.name}')

    # If the channel already exists, and the userID is in the channels dict, then we can check to see if we need to delete the channel
    elif before.channel and before.channel.id in user_channels.values():
        # Gets the channel based on the channelID
        channel = bot.get_channel(before.channel.id)

        # If the channel exists and is empty, then the channel is deleted
        if channel and len(channel.members) == 0:
            # Deletes the channel
            await channel.delete()
            # Gets and deletes the userID from the channel dict
            user_id = next(user for user, channel_id in user_channels.items() if channel_id == before.channel.id)
            del user_channels[user_id]
            print(f'Deleted empty voice channel: {channel.name}')

# Runs the bot code
bot.run('BOT TOKEN')