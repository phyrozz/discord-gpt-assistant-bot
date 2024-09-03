import discord
import os
import dynamo
import assistants

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    server_id = str(message.guild.id)

    if dynamo.check_guild(server_id):
        thread_id = dynamo.retrieve_thread_id(server_id)
        reply = assistants.handle_response(thread_id, message.content)

    else:
        thread = assistants.create_thread()
        reply = assistants.handle_response(thread.id, message.content)

    await message.channel.send(reply)

client.run(os.environ.get("DISCORD_API_KEY"))

