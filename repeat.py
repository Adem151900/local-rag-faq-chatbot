import sys
from rag_answer import ask

question = " ".join(sys.argv[1:])
for i in range(5):
    print(i + 1, "|", ask(question)[0].replace("\n", " "))