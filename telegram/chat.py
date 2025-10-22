import asyncio
import random
import string
from telegram import Bot

BOT_TOKEN = "8193710506:AAG8oEAKDwLba487Xm0qsMKcmbkYhvO0CEE"

bot = Bot(token=BOT_TOKEN)

chat_ids = [
    1005811588,
    # 7106247750,
    # 1684951303,
    # 1434799484
]

def generate_word(length=5):
    """Generate a random lowercase word of given length"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

async def main():
    for i in range(1, 1000):
        word = generate_word(random.randint(3, 8))
        text = f"{i}. {word}"
        
        for chat_id in chat_ids:
            msg = await bot.send_message(chat_id=chat_id, text=text)
            print(f"Sent message id {msg.message_id} to chat {chat_id}")
            await asyncio.sleep(0.1)  # wait 1 second before sending to next user

        await asyncio.sleep(0.1)  # optional: wait 1 second before next batch
    
asyncio.run(main())
