from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

print("🧠 Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded")


def retrieve(query, top_k=3):

    print("\n🔍 RETRIEVER STARTED")
    print("❓ QUERY:", query)

    # 🔥 THIS WAS MISSING BEFORE
    query_embedding = model.encode(query).tolist()

    print("📌 Embedding generated (first 5 values):", query_embedding[:5])

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/match_documents",
        json={
            "query_embedding": query_embedding,
            "match_count": top_k
        },
        headers=HEADERS
    )

    print("📡 STATUS:", response.status_code)

    if response.status_code != 200:
        print("❌ ERROR:", response.text)
        return []

    results = response.json()

    print("\n📦 TOP CHUNKS:")

    for i, r in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print("📚 BOOK:", r.get("book_name", "Unknown"))
        print("📄 CONTENT:", r["content"][:300])

    return results


if __name__ == "__main__":

    while True:
        q = input("\nAsk: ")
        if q.lower() == "exit":
            break

        retrieve(q)