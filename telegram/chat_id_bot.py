import asyncio
from telegram import Bot

BOT_TOKEN = "8193710506:AAG8oEAKDwLba487Xm0qsMKcmbkYhvO0CEE"
bot = Bot(token=BOT_TOKEN)

async def main():
    updates = await bot.get_updates()  
    for update in updates:
        if update.message:
            print("From username:", update.message.from_user.username)
            print("Chat ID:", update.message.chat.id)


asyncio.run(main())
