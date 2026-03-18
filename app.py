import requests
import streamlit as st

DEFAULT_LOCAL_URL = "http://127.0.0.1:8008/chat"

st.set_page_config(
    page_title="Sarika's RAG Portfolio Assistant",
    page_icon="🤖",
    layout="centered",
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")

    api_url = st.text_input("Server URL", value=DEFAULT_LOCAL_URL)
    st.caption("Run `python local_chat_server.py` before using this.")

    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("**About**")
    st.caption(
        "This is a RAG-powered chatbot that answers questions about "
        "Sarika S Shirolkar's portfolio using a local knowledge base "
        "and an LLM backend."
    )

# ── Chat history ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Sarika's RAG Portfolio Assistant")
st.caption("Ask me anything about Sarika's experience, projects, or skills.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            st.caption(f"Sources: {', '.join(msg['sources'])}")

# ── Input ──────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about experience, projects, skills..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    api_url,
                    json={"question": prompt},
                    timeout=60,
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])
            except requests.exceptions.ConnectionError:
                answer = (
                    "Could not reach the backend. "
                    "Make sure the server is running at: `" + api_url + "`"
                )
                sources = []
            except requests.exceptions.Timeout:
                answer = "The backend took too long to respond. Please try again."
                sources = []
            except Exception as e:
                answer = f"Something went wrong: {e}"
                sources = []

        st.markdown(answer)
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
