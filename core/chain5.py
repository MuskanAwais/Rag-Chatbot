from .memory2 import create_chat, save_message, get_chat_history
from .retriever1 import retrieve
from .prompt3 import build_prompt
from .llm4 import ask_mistral


def run_chain(chat_id, query):

    print("\n==============================")
    print("🚀 NEW REQUEST")
    print("==============================")

    # 1. MEMORY
    history = get_chat_history(chat_id)
    print("\n🧠 HISTORY LOADED")

    history_text = "\n".join(
        [f"{h['role']}: {h['message']}" for h in history]
    )

    # 2. RETRIEVER
    chunks = retrieve(query)

    context = "\n\n".join(
        [c["content"] if isinstance(c, dict) else c for c in chunks]
    )

    # 3. PROMPT
    prompt = build_prompt(query, context, history_text)

    print("\n📝 PROMPT READY")

    # 4. LLM
    answer = ask_mistral(prompt)

    if not answer:
        answer = "Sorry, I couldn't generate a response."

    print("\n✅ ANSWER:", answer)

    # 5. SAVE MEMORY
    save_message(chat_id, "user", query)
    save_message(chat_id, "assistant", answer)

    print("\n💾 MEMORY UPDATED")

    return answer