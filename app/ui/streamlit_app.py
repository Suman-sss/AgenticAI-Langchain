import requests
import streamlit as st


API_URL = "http://localhost:8000/api/v1/chat"

st.set_page_config(page_title="Agentic Beginner", page_icon="🤖", layout="centered")

st.title("Agentic Knowledge Assistant")
st.write("A beginner agentic AI project with UI, API, database, and retrieval-ready architecture.")

if "session_id" not in st.session_state:
    st.session_state.session_id = "demo-session-1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            st.caption("Sources:")
            for item in message["sources"]:
                st.write(f"- {item['source']}")
                st.caption(item["content"])

user_input = st.chat_input("Ask a question")

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(
            API_URL,
            json={
                "session_id": st.session_state.session_id,
                "message": user_input,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        assistant_text = data["response"]
        assistant_sources = data.get("sources", [])
    except requests.RequestException as exc:
        assistant_text = f"Error calling API: {exc}"
        assistant_sources = []

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_text,
            "sources": assistant_sources,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_text)
        if assistant_sources:
            st.caption("Sources:")
            for item in assistant_sources:
                st.write(f"- {item['source']}")
                st.caption(item["content"])
