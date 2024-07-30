import streamlit as st
from auth import authenticate
from dashboard import render_dashboard
from quizzes import render_quizzes
from register_page import render_register_page
from courses_page import render_courses_page

# Function to initialize session state variables if not already set
def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'show_register_page' not in st.session_state:
        st.session_state['show_register_page'] = False

# Login and registration section
def login_registration_section():
    if st.session_state['show_register_page']:
        render_register_page()
    else:
        st.title("Login or Register")
        
        if not st.session_state['authenticated']:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                user = authenticate(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = user[0]
                    st.success("Logged in successfully")
                else:
                    st.error("Invalid username or password")

            if st.button("Register"):
                st.session_state['show_register_page'] = True
                st.experimental_rerun()

# Main function for rendering different sections based on user state
def main():
    initialize_session_state()
    
    # If not authenticated, show login/registration section
    if not st.session_state['authenticated']:
        login_registration_section()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Quizzes", "Courses", "Logout"])

        if page == "Home":
            st.title("Home")
            st.write("Welcome to the Online Learning Platform")

        elif page == "Dashboard":
            render_dashboard(st.session_state['user_id'])

        elif page == "Quizzes":
            st.sidebar.subheader("Select a course")
            course_names = ["Machine Learning", "Python Programming", "Data Structures", "Web Development", "Database Systems"]
            course_id = st.sidebar.selectbox("Courses", range(1, len(course_names) + 1), format_func=lambda x: course_names[x - 1])
            render_quizzes(st.session_state['user_id'], course_id)

        elif page == "Courses":
            render_courses_page(st.session_state['user_id'])

        elif page == "Logout":
            st.session_state['authenticated'] = False
            st.session_state['user_id'] = None
            st.success("Logged out successfully")

if __name__ == '__main__':
    main()
