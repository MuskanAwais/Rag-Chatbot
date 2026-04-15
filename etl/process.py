# =========================
# PROCESS FILE
# =========================

import os
import PyPDF2
import re
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import logging

# =========================
# LOGGER SETUP
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# load env
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH")

# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x00", "")
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# -------------------------
# LOAD PDFs
# -------------------------
def load_pdfs(folder_path):

    logger.info("📄 Loading PDFs...")

    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):

            logger.info(f"📘 Reading: {file}")

            path = os.path.join(folder_path, file)

            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)

                text = ""

                # progress per page
                for page in tqdm(reader.pages, desc=f"Reading {file}"):
                    page_text = page.extract_text()

                    if page_text:
                        text += clean_text(page_text) + "\n"

                documents.append({
                    "book_name": file,
                    "text": text
                })

    logger.info(f"✅ Loaded {len(documents)} books")

    return documents

# -------------------------
# CHUNK TEXT
# -------------------------
def chunk_text(documents, chunk_size=200):

    logger.info("✂ Chunking text...")

    all_chunks = []

    for doc in documents:

        words = doc["text"].split()

        # progress per chunk
        for i in tqdm(range(0, len(words), chunk_size), desc=f"Chunking {doc['book_name']}"):

            chunk = " ".join(words[i:i+chunk_size])
            chunk = clean_text(chunk)

            if chunk.strip():
                all_chunks.append({
                    "book_name": doc["book_name"],
                    "chunk_no": i // chunk_size,
                    "content": chunk
                })

    logger.info(f"📊 Total chunks created: {len(all_chunks)}")

    return all_chunks

# -------------------------
# EMBEDDINGS
# -------------------------
def create_embeddings(chunks):

    logger.info("🧠 Creating embeddings...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [c["content"] for c in chunks]

    # progress bar for embeddings
    embeddings = []

    for text in tqdm(texts, desc="Embedding Progress"):
        emb = model.encode(text)
        embeddings.append(emb)

    logger.info(f"📊 Total embeddings created: {len(embeddings)}")

    return embeddings

# -------------------------
# MAIN FUNCTION
# -------------------------
def run_processing():

    logger.info("🚀 PROCESS STARTED")

    documents = load_pdfs(DATA_PATH)

    chunks = chunk_text(documents)

    embeddings = create_embeddings(chunks)

    logger.info("🎉 PROCESS COMPLETED")

    return chunks, embeddings


# -------------------------
# TEST RUN
# -------------------------
if __name__ == "__main__":

    chunks, embeddings = run_processing()

    logger.info(f"Final chunks: {len(chunks)}")
    logger.info(f"Final embeddings: {len(embeddings)}")