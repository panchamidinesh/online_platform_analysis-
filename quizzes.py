import sqlite3
import streamlit as st

def get_quiz_options(quiz_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT option1, option2, option3, option4 FROM quizzes WHERE id=?", (quiz_id,))
    options = cursor.fetchone()
    conn.close()
    return options

def get_quizzes(course_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM quizzes WHERE course_id=?", (course_id,))
    quizzes = cursor.fetchall()
    conn.close()
    return quizzes

def submit_quiz(user_id, quiz_id, selected_option):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT option1, option2, option3, option4, correct_option FROM quizzes WHERE id=?", (quiz_id,))
        options = cursor.fetchone()
        correct_option = options[4]
        selected_option_index = options.index(selected_option) + 1  # Convert option to index (1-based)
        score = 1 if selected_option_index == correct_option else 0
        cursor.execute("INSERT INTO quiz_scores (user_id, quiz_id, score) VALUES (?, ?, ?)", (user_id, quiz_id, score))
        conn.commit()
        conn.close()
        return score, correct_option
    except sqlite3.IntegrityError:
        conn.close()
        return None, None

def get_user_courses(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT course_id FROM user_courses WHERE user_id=?", (user_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses

def register_course(user_id, course_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO user_courses (user_id, course_id) VALUES (?, ?)", (user_id, course_id))
    conn.commit()
    conn.close()

def reset_quiz_scores(user_id, course_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM quiz_scores 
        WHERE user_id=? 
        AND quiz_id IN (SELECT id FROM quizzes WHERE course_id=?)
    """, (user_id, course_id))
    conn.commit()
    conn.close()

def render_quizzes(user_id, course_id):
    # Check if the user is enrolled in the selected course
    user_courses = get_user_courses(user_id)
    enrolled_course_ids = [course[0] for course in user_courses]
    
    if course_id not in enrolled_course_ids:
        # Show popup to register for the course
        st.warning("You are not enrolled in this course.")
        if st.button("Register for this course"):
            register_course(user_id, course_id)
            st.success("Successfully registered for this course. Please refresh the page.")
        return
    
    # User is enrolled in the course, proceed to render quizzes
    quizzes = get_quizzes(course_id)
    
    for quiz_id, question in quizzes:
        st.subheader(question)
        options = get_quiz_options(quiz_id)
        selected_option = st.radio(f"Options for question {quiz_id}", options, key=f"options_{quiz_id}")
        
        submit_button_key = f"submit_button_{quiz_id}"  # Unique key for each submit button
        
        if st.button("Submit Answer", key=submit_button_key):
            score, correct_option = submit_quiz(user_id, quiz_id, selected_option)
            if score is None:
                st.error("Already submitted, reset quiz to try again.")
            elif score == 1:
                st.success("Your answer is correct.")
            else:
                correct_answer = options[correct_option - 1]
                st.error(f"Your answer is incorrect. The correct answer is: {correct_answer}")
    
    reset_button_key = f"reset_button_{course_id}"  # Unique key for the reset button
    
    if st.button("Reset All Quizzes", key=reset_button_key):
        reset_quiz_scores(user_id, course_id)
        st.success("All quizzes for this course have been reset. You can take them again.")
