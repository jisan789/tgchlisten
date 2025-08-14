import json
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# Telegram API details
api_id = 28345038
api_hash = '6c438bbc256629655ca14d4f74de0541'
string_session = '1BVtsOHEBu7Ps0EP0Sf__DVSXwT5fI5EAW_XNszWyjecxwwtpq2FPkIBxs-6oxsnquDhS8txn2RLSlPtJhv124hKlLZ1Qfeg46sOzmWtcFb4s17ANgysjABnx6VNFcBrzzEqpP0TqRhOSH2BwnyniyaW7cvjcvBsW1JJiQUXddxqqb9DeamEcPB9KNsjf9gLIeWRJ9aLg14Lj5j81tWd3ylh7E2r-R4WutrcBs3ed-Bl5V6_laWPnoy8IiTE0rRdZ5guAO8JOLdn3dwyGAu1NbYru6_NrloqSx9Shod9gtr8pQk5le_KHCWhtqfUrQqClqnQo2axKolIOk3gTHFoDZOGJvJ2eiPM='

# Load mapping from external JSON
with open("mappings.json", "r") as f:
    mappings = json.load(f)

# Create Telegram client
client = TelegramClient(StringSession(string_session), api_id, api_hash)

print(f"Listening to {len(mappings)} channels:")
for m in mappings:
    print(f"  - {m['name']}")

async def forward_handler(event, target, name):
    try:
        await client.forward_messages(target, event.message)
        print(f"[{name}] Forwarded from {event.chat_id} to {target} -> message {event.id}")
    except FloodWaitError as e:
        print(f"[{name}] Flood wait for {e.seconds} seconds. Sleeping...")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"[{name}] Error: {e}")

def register_forward(source, target, name):
    @client.on(events.NewMessage(chats=source))
    async def handler(event):
        await forward_handler(event, target, name)

# Register each mapping with its own bound handler
for mapping in mappings:
    register_forward(mapping["source"], mapping["target"], mapping["name"])

print("Bot is running. Waiting for new messages...")
client.start()
client.run_until_disconnected()
