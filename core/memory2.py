import os
import requests
import uuid
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


# -------------------------
# CREATE CHAT
# -------------------------
def create_chat():
    chat_id = str(uuid.uuid4())
    print("🆔 New Chat ID:", chat_id)
    return chat_id


# -------------------------
# SAVE MESSAGE
# -------------------------
def save_message(chat_id, role, message):

    print(f"💾 Saving {role} message...")

    data = {
        "chat_id": chat_id,
        "role": role,
        "message": message
    }

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/chats",
        json=data,
        headers=HEADERS
    )

    if response.status_code != 201:
        print("❌ SAVE FAILED:", response.status_code, response.text)
    else:
        print("✅ Message saved")


# -------------------------
# GET HISTORY
# -------------------------
def get_chat_history(chat_id):

    print("🧠 Loading memory...")

    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/chats?chat_id=eq.{chat_id}&order=created_at.asc",
        headers=HEADERS
        

    )

    if res.status_code != 200:
        print("❌ MEMORY ERROR:", res.status_code, res.text)
        return []

    data = res.json()

    print(f"📜 Loaded {len(data)} messages")

    return data


'''print("\n==============================")
print("🧪 MEMORY SYSTEM TEST MODE")
print("==============================\n")

# 1️⃣ Create chat
chat_id = create_chat()
print("\n🆔 CHAT ID:", chat_id)

while True:

    user_input = input("\n💬 You: ")

    if user_input.lower() == "exit":
        print("👋 Exiting test mode")
        break

    # 2️⃣ Save user message
    save_message(chat_id, "user", user_input)

    # 3️⃣ Fake assistant reply (for testing)
    reply = f"I received: {user_input}"

    print("🤖 Bot:", reply)

    # 4️⃣ Save assistant message
    save_message(chat_id, "assistant", reply)

    # 5️⃣ Load history
    history = get_chat_history(chat_id)

    print("\n📜 CURRENT CHAT HISTORY:")
    for i, msg in enumerate(history):
        print(f"{i+1}. {msg['role']} → {msg['message']}")

    print("\n------------------------------")'''
