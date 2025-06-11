import streamlit as st
from db import init_db, SessionLocal, Task, Leave, User
from auth import login, signup
import datetime

init_db()

st.set_page_config(page_title="Task & Leave Manager", layout="wide")
st.title("✅ Task & Leave Manager")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    login()
    signup()
else:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    session = SessionLocal()
    current_user = session.query(User).filter_by(username=st.session_state.user).first()

    menu = st.sidebar.radio("Menu", ["Dashboard", "Tasks", "Leave", "Logout"])

    if menu == "Dashboard":
        st.subheader("Team Availability")
        leaves_today = session.query(Leave).filter_by(date=datetime.date.today()).all()
        if leaves_today:
            st.write("🔴 On Leave Today:")
            for leave in leaves_today:
                st.write(f"- {leave.user.username} ({leave.reason})")
        else:
            st.write("✅ Everyone is available today!")

    elif menu == "Tasks":
        st.subheader("Your Tasks")
        for task in current_user.tasks:
            st.write(f"- {task.title} | Status: {task.status}")
        new_task = st.text_input("New Task")
        if st.button("Add Task"):
            session.add(Task(title=new_task, user_id=current_user.id))
            session.commit()
            st.experimental_rerun()

    elif menu == "Leave":
        st.subheader("Apply for Leave")
        leave_date = st.date_input("Date", datetime.date.today())
        reason = st.text_input("Reason")
        if st.button("Apply Leave"):
            session.add(Leave(date=leave_date, reason=reason, user_id=current_user.id))
            session.commit()
            st.success("Leave applied.")
        st.subheader("Your Leave Requests")
        for leave in current_user.leaves:
            st.write(f"- {leave.date} | {leave.reason} | Approved: {leave.approved}")

    elif menu == "Logout":
        st.session_state.user = None
        st.experimental_rerun()

    session.close()
