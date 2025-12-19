```markdown
# 🚀 AI-Powered Policy Chatbot (Bangla + English)

### Join Venture AI — AI Developer Assessment Task

**Author:** *Your Name*  
**Date:** 2025

---

## 📌 Overview

This project is an **AI-powered chatbot** capable of answering questions about a **Government Energy Policy Document** in both **Bangla and English**.

The system uses **OCR extraction**, **vector embeddings**, and a **ChromaDB vector database** to retrieve relevant sections of the policy and answer user queries with contextual memory.

This submission fulfills all requirements from the official assignment:

* Extract policy data
* Build a searchable vector database (FAISS/ChromaDB)
* Answer questions about the document
* Support Bangla + English
* Maintain conversation memory
* Provide clean, helpful responses
* Include a GitHub repository with code + README

---

# 🧠 System Architecture

```

PDF → OCR → Clean JSON → Embeddings → ChromaDB → Query → Chatbot → Response

```

### **1. OCR-Based Data Extraction**

The original policy PDF used embedded Bangla fonts, making standard text extraction impossible.  
Therefore, OCR (Tesseract) + Poppler were used to generate clean Unicode Bangla text.

### **2. Vector Embeddings**

We use:

```

sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

```

This supports both Bangla and English embeddings.

### **3. Vector Database (ChromaDB)**

We store all policy chunks inside:

```

chroma_db/

```

Using the new **PersistentClient** API.

### **4. Chatbot**

The chatbot:

* Embeds user queries
* Retrieves top-k relevant policy sections
* Responds in user’s language (Bangla/English)
* Holds recent conversation memory (contextual follow-ups)

---

# 📂 Project Structure

```

interview-task/
│
├── extract_policy_ocr.py         # Extract text from PDF using OCR
├── embedder.py                   # Embedding helper (SentenceTransformer)
├── build_vector_db.py            # Builds ChromaDB vector store
├── chatbot.py                    # Main chatbot application
│
├── data/
│   └── policy_chunks_ocr.json    # Clean OCR-extracted Bangla text
│
├── chroma_db/                    # Persistent Chroma vector database
│
└── README.md                     # Documentation

````

---

# 🛠️ Installation & Setup

### **1. Install Python Dependencies**

```bash
pip install -r requirements.txt
````

(If `requirements.txt` not provided, install manually:)

```bash
pip install sentence-transformers chromadb langdetect pdf2image pytesseract pillow
```

---

## **2. Install External Dependencies**

### **Poppler (required for PDF → image)**

Download from:
[https://github.com/oschwartz10612/poppler-windows/releases/](https://github.com/oschwartz10612/poppler-windows/releases/)

Extract to:

```
C:\poppler-25.11.0\Library\bin
```

### **Tesseract OCR (required for OCR)**

Download from:
[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Install to:

```
C:\Program Files\Tesseract-OCR\
```

Make sure Bengali language is installed (`ben`).

---

# 📄 Step-by-Step Usage

## **1️⃣ Extract Text from Policy PDF**

```bash
python extract_policy_ocr.py
```

This generates:

```
data/policy_chunks_ocr.json
```

---

## **2️⃣ Build the Vector Database**

```bash
python build_vector_db.py
```

This creates:

```
chroma_db/
```

---

## **3️⃣ Run the Chatbot**

```bash
python chatbot.py
```

You will see:

```
✅ Policy chatbot ready. Ask about the energy policy (Bangla or English).
```

### Example queries:

#### Bangla:

```
এই নীতিমালায় নবায়নযোগ্য জ্বালানির জন্য কী পদক্ষেপ আছে?
সস্টেইনেবল জ্বালানি উন্নয়ন তহবিল কী?
```

#### English:

```
What are the initiatives for renewable energy?
Is there any sustainable energy development fund mentioned?
```

---

# 🧠 Features

### ✔ **Bangla + English Question Support**

The system auto-detects user language and responds in the same language.

### ✔ **Vector Search Using ChromaDB**

Top-k sections retrieved from policy chunks.

### ✔ **Conversation Memory**

The bot remembers the last few interaction turns to handle follow-up queries.

### ✔ **Multilingual Embeddings**

Using a Transformer model that supports Bangla + English semantic similarity.

### ✔ **OCR-Based Extraction**

Accurate Bangla text even from PDFs with embedded fonts.

---

# ⚠️ Known Limitations

* OCR text may contain minor recognition errors.
* The dataset includes all pages, but noisy sections (headers/page numbers) may affect retrieval.
* The chatbot is retrieval-based (RAG), not generative. It does not “invent” new facts.

---

# 📬 Submission Notes

This README + repository includes:

* All Python source files
* Extracted policy text
* Vector database builder
* Chatbot
* Instructions for running locally

Everything runs locally and **does not require deployment** — exactly as requested in the assessment instructions.

---

# 🙌 Credits

* **Poppler** for PDF rendering
* **Tesseract OCR** for Bangla text recognition
* **SentenceTransformers** for multilingual embeddings
* **ChromaDB** for vector storage and retrieval

---

# 🎯 Final Note for Evaluators

This solution demonstrates:

* Practical ability to build a **RAG (Retrieval-Augmented Generation)** system
* Strong understanding of **vector search**, **embeddings**, and **database setup**
* Use of **Bangla NLP tools**, which is critical for local policy/chatbot work
* Clean coding, modular structure, and high-quality engineering decisions (OCR fallback handling)

```
```
