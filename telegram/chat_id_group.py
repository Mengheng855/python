from pyrogram import Client

api_id = 28311458
api_hash = "7592b54a8227106c87a45cc744f42097"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

with app:
    for dialog in app.get_dialogs():
        print(dialog.chat.title, dialog.chat.id)