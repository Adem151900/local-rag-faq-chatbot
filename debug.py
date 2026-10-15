import sys
from rag_answer import is_not_english, is_injection, is_vague, normalize, THRESHOLD, ask
from rag import retrieve

q = " ".join(sys.argv[1:])
print("not english:", is_not_english(q))
print("injection  :", is_injection(q))
print("vague      :", is_vague(q))
n = normalize(q)
print("normalized :", n)
print("threshold  :", THRESHOLD)
for score, c in retrieve(n, k=3):
    print(f"{score:.2f} | {c['source']} | {c['text'][:90]}")
print("ANSWER     :", ask(q)[0])