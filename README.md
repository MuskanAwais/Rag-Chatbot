# 📚 BookMind AI — RAG Chatbot

An intelligent Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from uploaded books using embeddings, vector search, and an LLM (Mistral).

Built with:
- 🧠 Sentence Transformers (MiniLM embeddings)
- 🗄️ Supabase (Vector + memory storage)
- 🤖 Mistral AI (LLM responses)
- 📄 PDF book knowledge base
- 🎯 Streamlit frontend

---

# 🚀 Features

- 📖 Book-based question answering (no hallucination)
- 🔍 Semantic search using embeddings
- 🧠 Chat memory stored in Supabase
- 🤖 Mistral AI integration
- 💬 Streamlit chat UI
- 📦 Multi-book support

---

# 🏗️ Project Architecture

User Query  
→ Streamlit UI (app.py)  
→ chain5.py (main pipeline)  
→ Retriever (embeddings + Supabase vector search)  
→ Context + Chat History  
→ Prompt Builder  
→ Mistral LLM  
→ Final Answer  
→ UI Response  

---

# 📁 Project Structure

Rag_Chatbot/
│
├── app.py                  # Streamlit frontend
├── core/
│   ├── chain5.py          # Main pipeline
│   ├── memory2.py         # Chat memory (Supabase)
│   ├── retriever1.py      # Vector retrieval
│   ├── prompt3.py         # Prompt builder
│   ├── llm4.py            # Mistral API call
│   ├── Test6.py           # CLI testing
│   ├── __init__.py
│
├── data/
│   └── books/
├── etl/
├── .gitignore
└── README.md

---

# ⚙️ Installation

## Clone repo
git clone https://github.com/your-username/Rag_Chatbot.git
cd Rag_Chatbot

## Create environment
python -m venv venv
venv\Scripts\activate   # Windows

## Install dependencies
pip install streamlit requests python-dotenv sentence-transformers

---

# 🔐 Environment Variables

Create `.env` file:

SUPABASE_URL=your_supabase_url  
SUPABASE_KEY=your_supabase_key  
MISTRAL_KEY=your_mistral_api_key  

---

# ▶️ Run Project

## Streamlit UI
python -m streamlit run app.py

## CLI Test
python -m core.Test6

---

# 🧠 How It Works

1. User asks question
2. Convert query → embedding
3. Retrieve relevant book chunks
4. Load chat history
5. Build prompt
6. Send to Mistral
7. Return answer
8. Save memory

---

# 📊 Use Cases

- AI study assistant
- Book Q&A chatbot
- Leadership learning bot
- Entrepreneurship assistant

---

# ⚠️ Known Issues

- Large PDFs may trigger GitHub warning
- Needs internet for Supabase + Mistral API
- Embedding model loads on first run

---

# 🚀 Future Improvements

- Streaming responses (typing effect)
- Better memory summarization
- Source citations per answer
- Cloud deployment
- Faster retrieval optimization

---

# 👩‍💻 Author

Muskan Awais

---
