import discord
from discord.ext import commands
from api_key import discord_token
from chat import Chat
import random

random_slur = ["dumb", "lazy", "ugly", "fat", "stupid", "weird", "dull"]
 
client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
# set activity
activity = discord.Game(name="with humans")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=activity)

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # reply as user - functionality for bot, when message is .. and is in reply to someone
    if message.content == "..":
        if not message.reference:
            await message.reply("You need to reply to someone to use this command")
            return
        reference = message.reference.resolved
        
        # add the name of sender in front of message, to make it clear for chatbot who is sending the message
        reference.content = f"{reference.author.global_name} says {reference.content}"
        await bot_reply(message=reference, user_to_mention=message.author.mention)


    elif client.user.mentioned_in(message):
        # remove the mentioned user
        message.content = message.content.replace(client.user.name, "")
        # add the name of sender in front of message, to make it clear for chatbot who is sending the message
        message.content = f"{message.author.global_name} says {message.content}"
        await bot_chat(message=message)
    
    elif message.reference:
        reference = message.reference.resolved
        if reference.author == client.user:
            # add the name of sender in front of message, to make it clear for chatbot who is sending the message
            message.content = f"{message.author.global_name} says {message.content}"
            await bot_chat(message=message)
    
    elif message.content.startswith('.'):
        message.content = message.content[1:]
        # add the name of sender in front of message, to make it clear for chatbot who is sending the message
        message.content = f"{message.author.global_name} says {message.content}"
        await bot_chat(message=message)



pika = Chat()
async def bot_chat(message):
    async with message.channel.typing():
            response = pika.send_message(message.content)
            # reply to the person with response
            await message.reply(response)

async def bot_reply(message, user_to_mention):
    async with message.channel.typing():
            response = pika.send_message(f"{message.content}\nWhat should i reply to this, just tell the message nothing else")
            # reply to the person with response
            await message.reply(f"Since {user_to_mention} is too {random.choice(random_slur)} to reply, I will do it for them:\n{response}")

client.run(discord_token)