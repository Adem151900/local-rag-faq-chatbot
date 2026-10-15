import json, math, sys
import ollama

EMBED_MODEL = "nomic-embed-text"
INDEX = json.load(open("index.json", encoding="utf-8"))

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def retrieve(question, k=3):
    q = ollama.embed(model=EMBED_MODEL, input=question)["embeddings"][0]
    scored = [(cosine(q, c["vector"]), c) for c in INDEX]
    scored.sort(key=lambda s: s[0], reverse=True)
    return scored[:k]

if __name__ == "__main__":
    for score, c in retrieve(" ".join(sys.argv[1:])):
        print(f"{score:.2f} | {c['source']} | {c['text']}")