import discord
import os
import dynamo
import assistants
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with command prefix and intents
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Process commands first
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    if message.author == bot.user:
        return

    server_id = str(message.guild.id)
    channel_id = str(message.channel.id)

    # Check if the bot is allowed to respond in this channel
    if not dynamo.is_channel_allowed(server_id, channel_id):
        return

    if dynamo.check_guild(server_id):
        print(f"Retrieved existing thread: {server_id}")
        thread_id = dynamo.retrieve_thread_id(server_id)
        reply = await assistants.handle_response(thread_id, message.content)
    else:
        print("Created new thread")
        thread = await assistants.create_thread()
        dynamo.insert_guild(server_id, thread.id)
        reply = await assistants.handle_response(thread.id, message.content)

    await message.channel.send(reply)

    # Ensure the bot processes commands after handling the message
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def allow_channel(ctx):
    print("Allowed")
    server_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)

    dynamo.add_allowed_channel(server_id, channel_id)
    await ctx.send(f"Bot is now allowed to respond in {ctx.channel.mention}.")

@bot.command()
@commands.has_permissions(administrator=True)
async def disallow_channel(ctx):
    print("Disallowed")
    server_id = str(ctx.guild.id)
    channel_id = str(ctx.channel.id)

    dynamo.remove_allowed_channel(server_id, channel_id)
    await ctx.send(f"Bot is no longer allowed to respond in {ctx.channel.mention}.")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

bot.run(os.environ.get("DISCORD_API_KEY"))