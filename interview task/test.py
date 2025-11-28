import chromadb
from embedder import Embedder

client = chromadb.PersistentClient(path="chroma_db")
col = client.get_collection("policy_chunks")
embedder = Embedder()

q = "বাজেট"  # or some Bangla word you expect
emb = embedder.embed_one(q)

res = col.query(query_embeddings=[emb], n_results=2)
print(res["documents"][0][0])
