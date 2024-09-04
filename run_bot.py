import asyncio
import os
from bot_setup import bot
from discord.errors import ConnectionClosed

MAX_RETRIES = 5
BASE_WAIT_TIME = 2

async def run_bot():
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            await bot.start(os.environ.get("DISCORD_API_KEY"))
        except ConnectionClosed as e:
            retry_count += 1
            wait_time = BASE_WAIT_TIME * (2 ** (retry_count - 1))  # Exponential backoff
            print(f"Connection closed with error {e.code}. Retrying in {wait_time} seconds... ({retry_count}/{MAX_RETRIES})")
            await asyncio.sleep(wait_time)
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"An error occurred: {str(e)}. Retrying in {BASE_WAIT_TIME} seconds...")
            await asyncio.sleep(BASE_WAIT_TIME)
        else:
            # Reset retry count on successful connection
            retry_count = 0
            print("Connected successfully!")
            break
    else:
        print("Max retries exceeded. Exiting...")

# Start the bot with retry logic
if __name__ == "__main__":
    asyncio.run(run_bot())
