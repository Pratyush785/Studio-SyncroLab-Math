import streamlit as st
import google.generativeai as genai

# --- 1. THE LOCK (GOOGLE LOGIN) ---
# This stops anyone from using the bot until they sign in
if not st.user.is_logged_in:
    st.title("♾️ Studio SyncroLab Dual Core AI: powered by Gemini")
    st.subheader("Solve any Maths and Applied Mathematics problem")
    st.info("Please log in with your Google account to start solving.")
    # The 'google' argument tells Streamlit which provider to use
    st.button("Log in with Google", on_click=st.login, args=["google"])
    st.stop()

# --- 2. THE BRAIN (DUAL API PROTECTION) ---
# We pull your keys safely from Streamlit Secrets
try:
    API_KEYS = st.secrets["MY_KEYS"]
except:
    API_KEYS = ["AIzaSyAWwcT7ZR6I8O5i-K29qblj05jhMP1pvHg", "AIzaSyCHiwNQlEuAncqyE89i3Yt04FMpX_hOEmU"]

def get_working_model():
    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            return genai.GenerativeModel('gemini-2.5-flash')
        except:
            continue
    return None

model = get_working_model()

# --- 3. THE INTERFACE ---
st.set_page_config(page_title="Studio SyncroLab", page_icon="♾️")

# Header with User Name and Logout
col1, col2 = st.columns([0.8, 0.2])
col1.title(f"Welcome, {st.user.name}!")
col2.button("Log out", on_click=st.logout)

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. THE SOLVER ---
if prompt := st.chat_input("Ask any math or engineering question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            with st.spinner("Analyzing..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("Engine busy. Please try again in a moment.")
        else:
            st.error("Connection Error: No active API found.")