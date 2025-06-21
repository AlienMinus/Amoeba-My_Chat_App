# app.py
import streamlit as st

from auth_db import create_users_table, add_user, verify_user
from chat_db import (
    create_chat_table, add_message, get_messages_between,
    mark_user_active, remove_user_active, get_active_users
)

create_users_table()
create_chat_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ----------- Login / Signup ----------
def login():
    st.subheader("🔐 Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        valid, role = verify_user(user, pwd)
        if valid:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.role = role
            mark_user_active(user)
            st.success(f"Welcome, {user}!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

def signup():
    st.subheader("🆕 Sign Up")
    new_user = st.text_input("Username", key="signup_user")
    new_pass = st.text_input("Password", type="password", key="signup_pass")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
    role = st.selectbox("Role", ["viewer", "developer"], key="signup_role")
    if st.button("Register"):
        if new_pass != confirm:
            st.error("Passwords do not match")
        elif add_user(new_user, new_pass, role):
            st.success("Account created. Please login.")
            st.rerun()
        else:
            st.warning("Username already exists.")

# ---------- Logout ----------
def logout():
    remove_user_active(st.session_state.username)
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.success("Logged out.")
    st.rerun()

# ----------- Chat Room ----------
def chat_room():
    st.title("🫧 Amoeba Chats")

    st.sidebar.write(f"👤 `{st.session_state.username}`")
    st.sidebar.write(f"🛡️️ `{st.session_state.role}`")
    if st.sidebar.button("Logout"):
        logout()

    active_users = get_active_users(st.session_state.username)
    selected_user = st.selectbox("\U0001F465 Chat with", active_users) if active_users else None

    if not selected_user:
        st.info("Waiting for user selection...")
        return

    st.markdown(f"**Chatting with:** `{selected_user}`")
    chat_history = get_messages_between(st.session_state.username, selected_user)

    for sender, role, msg, time in chat_history:
        with st.chat_message("user" if sender == st.session_state.username else "assistant"):
            st.markdown(f"**{sender}** ({role}) — _{time}_")
            st.markdown(msg)

    user_msg = st.chat_input("Type your message")
    if user_msg:
        add_message(st.session_state.username, selected_user, st.session_state.role, user_msg)
        st.rerun()

# ---------- Entry ----------
def main():
    st.set_page_config("🫧 Amoeba - My Chat App", layout="centered")
    if st.session_state.logged_in:
        chat_room()
    else:
        option = st.radio("Select", ["Login", "Sign Up"], horizontal=True)
        if option == "Login":
            login()
        else:
            signup()

if __name__ == "__main__":
    main()
