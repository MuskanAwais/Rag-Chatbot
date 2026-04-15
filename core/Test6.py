from chain5 import run_chain
from memory2 import create_chat

print("\n==============================")
print("🤖 BOOKMIND AI CHAT STARTED")
print("==============================\n")

chat_id = create_chat()
print("🆔 CHAT ID:", chat_id)

while True:

    try:
        q = input("\n💬 You: ")

        if q.lower().strip() in ["exit", "quit", "stop"]:
            print("\n👋 Chat ended. Goodbye!")
            break

        if not q.strip():
            print("⚠️ Please enter a valid question.")
            continue

        ans = run_chain(chat_id, q)

        print("\n🤖 BOT:", ans)
        print("\n------------------------------")

    except Exception as e:
        print("\n❌ ERROR OCCURRED:", str(e))
        print("🔄 System recovered, continue chatting...\n")