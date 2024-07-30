import sqlite3
import streamlit as st
import pandas as pd

def get_user_progress(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT courses.name, user_progress.progress 
    FROM user_progress 
    JOIN courses ON user_progress.course_id = courses.id 
    WHERE user_progress.user_id=?""", (user_id,))
    progress = cursor.fetchall()
    conn.close()
    return progress

def get_quiz_scores(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT courses.name, quizzes.question, quiz_scores.score 
    FROM quiz_scores 
    JOIN quizzes ON quiz_scores.quiz_id = quizzes.id 
    JOIN courses ON quizzes.course_id = courses.id 
    WHERE quiz_scores.user_id=?""", (user_id,))
    scores = cursor.fetchall()
    conn.close()
    return scores

def get_courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_user_courses(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT courses.id, courses.name 
    FROM user_courses 
    JOIN courses ON user_courses.course_id = courses.id 
    WHERE user_courses.user_id=?""", (user_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses

def register_course(user_id, course_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user_courses (user_id, course_id) VALUES (?, ?)", (user_id, course_id))
    conn.commit()
    conn.close()

def render_dashboard(user_id):
    st.title("Dashboard")

    # Course registration form
    st.header("Register for a Course")
    courses = get_courses()
    course_options = {course[1]: course[0] for course in courses}
    selected_course = st.selectbox("Select a course to register", course_options.keys())
    if st.button("Register"):
        register_course(user_id, course_options[selected_course])
        st.success(f"Successfully registered for {selected_course}")

    # Get user progress for all courses
    progress = get_user_progress(user_id)
    df_progress = pd.DataFrame(progress, columns=["Course", "Progress"])
    
    # Display course progress as a bar chart
    st.header("Course Progress")
    st.bar_chart(df_progress.set_index("Course"))

    # Get courses the user is enrolled in
    user_courses = get_user_courses(user_id)
    if user_courses:
        enrolled_courses = {course[1]: course[0] for course in user_courses}
        
        # Dropdown to select a course
        selected_course = st.selectbox("Select a course to view quiz scores", enrolled_courses.keys())
        
        # Get and filter quiz scores for the selected course
        scores = get_quiz_scores(user_id)
        df_scores = pd.DataFrame(scores, columns=["Course", "Question", "Score"])
        df_scores_filtered = df_scores[df_scores["Course"] == selected_course]
        
        total_score = df_scores_filtered["Score"].sum()
        
        # Display quiz scores for the selected course
        st.header(f"Quiz Scores for {selected_course}")
        st.text(f'Total score: {total_score}/5')
        st.dataframe(df_scores_filtered[["Question", "Score"]].set_index("Question"))
    else:
        st.warning("You are not enrolled in any courses.")

