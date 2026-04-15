import os
import PyPDF2
import numpy as np
import time 
from sentence_transformers import SentenceTransformer
import requests

# =========================
# SUPABASE CONFIG (ADD YOURS)
# =========================
SUPABASE_URL = "https://uouuvxwnucuuqmjfhnhl.supabase.co"
SUPABASE_KEY = "sb_publishable_lk4U4iTCsjC3sRY7GYz_hQ_5zn_wDnG"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}



# =========================
# LOAD PDFs
# =========================
def load_pdfs(folder_path):
    text = ""

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            path = os.path.join(folder_path, file)

            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

    return text

# =========================
# CHUNK TEXT
# =========================
def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))

    return chunks

# =========================
# FAST BATCH SUPABASE STORE
# =========================
def store_in_supabase(chunks, embeddings):

    url = f"{SUPABASE_URL}/rest/v1/documents"

    BATCH_SIZE = 10
    batch = []

    for i, chunk in enumerate(chunks):

        batch.append({
            "content": chunk,
            "embedding": embeddings[i].tolist()
        })

        # send batch
        if len(batch) == BATCH_SIZE or i == len(chunks) - 1:

            try:
                res = requests.post(url, json=batch, headers=HEADERS)

                if res.status_code in [200, 201]:
                    print(f"✔ Stored batch of {len(batch)} chunks")
                else:
                    print("❌ Error:", res.text)

            except Exception as e:
                print("⚠ Connection error:", e)

            batch = []
            time.sleep(0.2)

# =========================
# MAIN PIPELINE
# =========================
def main():

    print("📄 Loading PDFs...")
    text = load_pdfs(r"D:\Python\Rag_Chatbot\data\books")

    print("✂ Chunking text...")
    chunks = chunk_text(text)

    print(f"📊 Total chunks: {len(chunks)}")

    print("🧠 Creating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    print(f"📊 Total embeddings: {len(embeddings)}")

    print("☁ Storing in Supabase...")
    store_in_supabase(chunks, embeddings)

    print("🎉 ETL Completed Successfully!")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()