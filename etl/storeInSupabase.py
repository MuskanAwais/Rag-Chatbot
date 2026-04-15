# =========================
# STORE FILE (SUPABASE)
# =========================

import os
import time
import requests
import hashlib
from dotenv import load_dotenv

# load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# -------------------------
# UNIQUE ID (NO DUPLICATION)
# -------------------------
def generate_id(text):
    return hashlib.md5(text.encode()).hexdigest()

# -------------------------
# STORE FUNCTION
# -------------------------
def store_in_supabase(chunks, embeddings):

    print("☁ Storing in Supabase...")

    url = f"{SUPABASE_URL}/rest/v1/documents"

    BATCH_SIZE = 10
    batch = []

    for i, chunk in enumerate(chunks):

        # unique id (book + chunk_no)
        unique_string = f"{chunk['book_name']}_{chunk['chunk_no']}"
        doc_id = generate_id(unique_string)

        batch.append({
            "id": doc_id,
            "book_name": chunk["book_name"],   # 🔥 new column
            "chunk_no": chunk["chunk_no"],     # 🔥 new column
            "content": chunk["content"],
            "embedding": embeddings[i].tolist()
        })

        # send batch
        if len(batch) == BATCH_SIZE or i == len(chunks) - 1:

            try:
                res = requests.post(url, json=batch, headers=HEADERS)

                if res.status_code in [200, 201]:
                    print(f"✔ Stored batch of {len(batch)}")
                else:
                    print("❌ Error:", res.text)

            except Exception as e:
                print("⚠ Connection error:", e)

            batch = []
            time.sleep(0.2)