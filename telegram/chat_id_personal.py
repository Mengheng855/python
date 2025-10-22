from pyrogram import Client
api_id = 28311458        
api_hash = "7592b54a8227106c87a45cc744f42097" 
app = Client("my_account", api_id=api_id, api_hash=api_hash)
usernames = [
    "@huch_hernandez",
    # '@Watsuub'
    # '@ounkoemtong' 
    # '@kyros123456789'
]
with app:
    me = app.get_me()
    print("Your own chat_id:", me.id)
    for username in usernames:
        try:
            user = app.get_users(username)
            print(f"{user.username} chat_id:", user.id)
        except Exception as e:
            print(f"Error getting {username}: {e}")

