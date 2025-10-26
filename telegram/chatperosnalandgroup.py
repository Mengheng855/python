import asyncio
import random
import time
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError

api_id = 28311458
api_hash = "7592b54a8227106c87a45cc744f42097"
app = Client("my_account", api_id=api_id, api_hash=api_hash)

chat_ids = [
    # 7106247750
    # 1373268619
    # 1316815720
    -1003174944925
]
word=input('Enter your message: ')

MIN_DELAY = 1.5      
MAX_DELAY = 4.0      
MAX_RETRIES = 3      

async def safe_send(chat_id, text):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await app.send_message(chat_id, text)
            return True
        except FloodWait as fw:
            wait = fw.x if hasattr(fw, "x") else fw.value  
            print(f"[FloodWait] need to wait {wait} seconds — sleeping...")
            await asyncio.sleep(wait + 1)
        except RPCError as e:
       
            print(f"[RPCError] attempt {attempt} failed: {e}")
            await asyncio.sleep(2 ** attempt) 
        except Exception as e:
            print(f"[Unexpected error] {e}")
            return False
    print("Max retries reached, message not sent.")
    return False

async def main():
    await app.start()
    x = int(input("Enter number of messages to send: "))
    for i in range(1, x + 1):
        message = f"{i}. {word}"
        for chat_id in chat_ids:
            ok = await safe_send(chat_id, message)
            print(f"Sent to {chat_id}: {message}" if ok else f"Failed to send to {chat_id}")
       
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"Sleeping {delay:.2f}s before next message...")
        await asyncio.sleep(delay)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
