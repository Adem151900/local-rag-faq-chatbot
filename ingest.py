import json, os, re
import ollama

EMBED_MODEL = "nomic-embed-text"
chunks = []

for name in os.listdir("docs"):
    if not name.endswith(".txt"):
        continue
    text = open(os.path.join("docs", name), encoding="utf-8").read()
    for part in re.split(r"\n\s*\n", text):
        part = part.strip()
        if part:
            vector = ollama.embed(model=EMBED_MODEL, input=part)["embeddings"][0]
            chunks.append({"source": name, "text": part, "vector": vector})

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f)

print(f"Indexed {len(chunks)} chunks")