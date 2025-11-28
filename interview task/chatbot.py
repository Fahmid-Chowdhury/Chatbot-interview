# chatbot.py

import chromadb
from langdetect import detect, LangDetectException

from embedder import Embedder


class PolicyChatbot:
    """
    Simple retrieval-based chatbot for the energy policy document.
    - Uses ChromaDB (PersistentClient) as vector store
    - Uses SentenceTransformer embeddings (via Embedder)
    - Handles Bangla + English
    - Keeps a small conversation memory to give context to follow-up questions
    """

    def __init__(
        self,
        persist_dir: str = "chroma_db",
        collection_name: str = "policy_chunks",
        memory_size: int = 5,
    ):
        # Connect to existing Chroma DB
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

        self.embedder = Embedder()
        self.memory = []  # list of dicts: {"user": ..., "bot": ...}
        self.memory_size = memory_size

    # ----------------- Memory handling -----------------

    def add_to_memory(self, user_msg: str, bot_msg: str):
        """Store last few turns of conversation."""
        self.memory.append({"user": user_msg, "bot": bot_msg})
        # Keep only last `memory_size` turns
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

    def build_search_query(self, user_query: str) -> str:
        """
        Use conversation memory to build a better search query.
        Very simple logic:
        - If there is a previous user query, concatenate it with the current one.
        """
        if not self.memory:
            return user_query

        last_user_query = self.memory[-1]["user"]
        # Combine last question + current question to give context for follow-ups like "What about renewables?"
        combined = f"{last_user_query} | {user_query}"
        return combined

    # ----------------- Utility funcs -----------------

    def detect_language(self, text: str) -> str:
        """Return 'bn' for Bangla, 'en' for English, fallback 'en' on error."""
        try:
            lang = detect(text)
            return lang
        except LangDetectException:
            return "en"

    def search_policy(self, query: str, top_k: int = 3):
        """
        Run vector search over policy chunks.
        Returns list of (text, page) tuples.
        """
        # Build context-aware query
        search_text = self.build_search_query(query)

        query_embedding = self.embedder.embed_one(search_text)

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]

        hits = []
        for doc, meta in zip(docs, metas):
            page = meta.get("page", None)
            hits.append((doc, page))

        return hits

    # ----------------- Core answer function -----------------

    def answer(self, user_query: str) -> str:
        """
        Main method:
        - Detect language
        - Retrieve relevant policy sections
        - Format answer in same language
        - Update memory
        """
        lang = self.detect_language(user_query)
        hits = self.search_policy(user_query, top_k=3)

        if not hits:
            if lang == "bn":
                reply = "দুঃখিত, নীতিমালার মধ্যে প্রাসঙ্গিক তথ্য খুঁজে পাইনি। প্রশ্নটা একটু ভেঙে বলবেন?"
            else:
                reply = "Sorry, I couldn't find relevant information in the policy document. Could you rephrase your question?"
            self.add_to_memory(user_query, reply)
            return reply

        if lang == "bn":
            header = "নীতিমালার প্রাসঙ্গিক অংশগুলো নিচে দেওয়া হলো:\n"
            parts = []
            for doc, page in hits:
                parts.append(f"[পৃষ্ঠা {page}] {doc}")
            body = "\n\n".join(parts)
            reply = header + body
        else:
            header = "Here are the most relevant sections from the policy document:\n"
            parts = []
            for doc, page in hits:
                parts.append(f"[Page {page}] {doc}")
            body = "\n\n".join(parts)
            reply = header + body

        # Update memory
        self.add_to_memory(user_query, reply)
        return reply


# ----------------- Simple CLI loop -----------------


def main():
    bot = PolicyChatbot(
        persist_dir="chroma_db",
        collection_name="policy_chunks",
        memory_size=5,
    )

    print("✅ Policy chatbot ready. Ask about the energy policy (Bangla or English).")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_query.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        if not user_query:
            continue

        reply = bot.answer(user_query)
        print(f"\nBot: {reply}\n")


if __name__ == "__main__":
    main()
