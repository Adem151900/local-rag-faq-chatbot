import streamlit as st
import ollama
from rag_answer import ask, is_not_english, NOT_ENGLISH, CLARIFY, REFUSAL, MODEL

st.title("School FAQ assistant")
st.caption("Runs locally with Ollama and RAG")


def make_standalone(question, history):
    """Turn a short follow-up like 'and when does it close?' into a full question."""
    if not history or len(question.split()) > 8:
        return question
    convo = "\n".join(f"{m['role']}: {m['content']}" for m in history[-4:])
    prompt = (
        "Rewrite the user's last question so it can be understood without the conversation. "
        "Replace words like 'it', 'that' or 'there' with what they refer to. "
        "If the question is already clear, return it unchanged. "
        "Output ONLY the rewritten question.\n\n"
        f"Conversation:\n{convo}\n\nLast question: {question}"
    )
    out = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},
    )
    return out["message"]["content"].strip().strip('"')


if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if question := st.chat_input("Ask a question"):
    # only real questions with real answers count as history
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m.get("valid", True)
    ][-6:]

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if is_not_english(question):
                answer = NOT_ENGLISH
            else:
                standalone = make_standalone(question, history)
                answer, _ = ask(standalone, history=history)
        st.write(answer)

    valid = answer not in (NOT_ENGLISH, CLARIFY, REFUSAL)
    st.session_state.messages.append({"role": "user", "content": question, "valid": valid})
    st.session_state.messages.append({"role": "assistant", "content": answer, "valid": valid})