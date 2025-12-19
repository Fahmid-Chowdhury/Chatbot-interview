# 🚀 RAG-Powered Policy Chatbot (Bangla + English)

### Join Venture AI — AI Developer Assessment Task

**Author:** *Your Name*
**Date:** 2025

---

## 📌 Overview

This AI-powered **chatbot** answers questions about a **Government Energy Policy Document** in **Bangla and English** using **OCR**, **vector embeddings**, and **ChromaDB** for retrieval.

Key Features:

* Extract policy data
* Build a searchable vector database (FAISS/ChromaDB)
* Multilingual support (Bangla/English)
* Conversation memory

---

## 🧠 System Architecture

```
PDF → OCR → Clean JSON → Embeddings → ChromaDB → Query → Chatbot → Response
```

**Steps:**

1. **OCR Extraction**: Extract text from PDF using Tesseract and Poppler.
2. **Vector Embeddings**: Using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` for Bangla/English.
3. **ChromaDB**: Store embeddings for fast retrieval.
4. **Chatbot**: Processes queries, retrieves relevant policy sections, and responds in the user’s language.

---

## 📂 Project Structure

```
interview-task/
├── extract_policy_ocr.py      # Extract text using OCR
├── embedder.py                # Helper for embeddings
├── build_vector_db.py         # Build ChromaDB store
├── chatbot.py                 # Main chatbot
├── data/policy_chunks_ocr.json # OCR-extracted text
└── chroma_db/                 # Chroma vector database
```

---

## 🛠️ Installation & Setup

### **1. Install Python Dependencies**

```bash
pip install -r requirements.txt
```

Manually:

```bash
pip install sentence-transformers chromadb langdetect pdf2image pytesseract pillow
```

### **2. External Dependencies**

* **Poppler** for PDF rendering
* **Tesseract OCR** for Bangla text extraction

---

## 📄 Usage

### **1. Extract Text**

```bash
python extract_policy_ocr.py
```

### **2. Build Vector DB**

```bash
python build_vector_db.py
```

### **3. Run Chatbot**

```bash
python chatbot.py
```

**Example Queries:**

#### Bangla:

```
এই নীতিমালায় নবায়নযোগ্য জ্বালানির জন্য কী পদক্ষেপ আছে?
```

#### English:

```
What are the initiatives for renewable energy?
```

---

## 🧠 Features

* **Bangla + English** support
* **Vector Search** via ChromaDB
* **Conversation Memory**
* **OCR-Based Extraction** for accurate Bangla text

---

## ⚠️ Known Limitations

* OCR text may have minor errors.
* The chatbot is retrieval-based (RAG), not generative.

---

## 📬 Submission Notes

The submission includes:

* Python files
* OCR-extracted text
* Vector DB setup
* Chatbot with instructions for local use

---

## 🙌 Credits

* **Poppler** for PDF rendering
* **Tesseract OCR** for Bangla text recognition
* **SentenceTransformers** for embeddings
* **ChromaDB** for vector storage

---

## 🎯 Final Note for Evaluators

This solution showcases:

* **RAG system** implementation
* Understanding of **vector search** and **database setup**
* **Bangla NLP tools** integration for local policy chatbot work
