from rag_answer import ask, MODEL

TESTS = [
    ("How many books can I take out at once?", ["5"], []),
    ("Is the library open on public holidays?", ["closed"], []),
    ("Which months are the tuition installments due?", ["December"], []),
    ("What documents do I bring when enrolling?", ["ID"], []),
    ("Can I extend my book loan twice?", ["2", "twice", "two"], []),
    ("How long does it take to get a certificate?", ["3 working", "three"], []),
    ("What's the weather like today?", [], ["sunny", "rainy", "degrees"]),
    ("Is there a cafeteria?", ["don't know", "administration"], []),
    ("I forgot to register on time, what now?", ["October 10"], []),
    ("Can I get a refund on tuition?", ["don't know", "administration"], []),
]

passed = 0
for question, any_of, none_of in TESTS:
    answer = ask(question)[0]
    ok = (not any_of or any(s.lower() in answer.lower() for s in any_of)) \
         and not any(s.lower() in answer.lower() for s in none_of)
    passed += ok
    print("PASS" if ok else "FAIL", "|", question)
    print("   ", answer.replace("\n", " "))

print(f"\nScore: {passed}/{len(TESTS)} with {MODEL}")