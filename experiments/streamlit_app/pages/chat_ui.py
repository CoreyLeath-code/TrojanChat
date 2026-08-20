import streamlit as st
from app.core.llm_client import LLMClient
from app.services.chat_service import ChatService
from streamlit_app.state import init_state

st.set_page_config(page_title="TrojanChat", layout="wide")
st.title("🏈 TrojanChat")

init_state()

llm = LLMClient(api_key=st.secrets["OPENAI_API_KEY"])
chat_service = ChatService(llm)

user_input = st.text_input("Discuss USC football")

if user_input:
    response = chat_service.respond(
        st.session_state.history,
        user_input
    )
    st.session_state.history += f"\nUser: {user_input}\nBot: {response}"
    st.markdown(response)