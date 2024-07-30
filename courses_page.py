import streamlit as st
import sqlite3

# Function to fetch course topics
def get_course_topics(course_id):
    topics = {
        1: [
            "Introduction to Machine Learning",
            "Supervised Learning",
            "Unsupervised Learning",
            "Neural Networks",
            "Decision Trees",
            "Ensemble Methods",
            "Dimensionality Reduction",
            "Model Evaluation and Selection",
            "Natural Language Processing",
            "Deep Learning"
        ],
        2: [
            "Introduction to Python",
            "Variables and Data Types",
            "Control Flow and Loops",
            "Functions and Modules",
            "Data Structures (Lists, Tuples, Dictionaries)",
            "File Handling",
            "Object-Oriented Programming",
            "Error Handling and Debugging",
            "Regular Expressions",
            "GUI Programming with Tkinter"
        ],
        3: [
            "Introduction to Data Structures",
            "Arrays and Strings",
            "Linked Lists",
            "Stacks and Queues",
            "Trees and Binary Trees",
            "Graphs and Graph Algorithms",
            "Sorting Algorithms",
            "Searching Algorithms",
            "Dynamic Programming",
            "Greedy Algorithms"
        ],
        4: [
            "Introduction to Web Development",
            "HTML and CSS Basics",
            "CSS Advanced Techniques",
            "JavaScript Fundamentals",
            "DOM Manipulation",
            "Web APIs (Fetch, Local Storage)",
            "Frontend Frameworks (React, Angular, Vue)",
            "Backend Development (Node.js, Express)",
            "RESTful APIs",
            "Web Security"
        ],
        5: [
            "Introduction to Databases",
            "Relational Database Concepts",
            "SQL Basics (Queries, Joins, Aggregations)",
            "Database Design and Normalization",
            "Indexing and Performance Optimization",
            "Transactions and Concurrency Control",
            "NoSQL Databases (MongoDB, Redis)",
            "Advanced Database Topics",
            "Data Warehousing",
            "Big Data and Distributed Databases"
        ]
    }
    
    return topics.get(course_id, [])

# Function to update progress based on completed topics
def update_progress(cursor, user_id, course_id, completed_topics):
    # Check if there's existing progress for this user and course
    cursor.execute("""
    SELECT COUNT(*) FROM user_progress WHERE user_id = ? AND course_id = ?
    """, (user_id, course_id))
    result = cursor.fetchone()

    if result[0] == 0:
        # If no existing progress entry, insert a new row
        cursor.execute("""
        INSERT INTO user_progress (user_id, course_id, progress, completed_topics)
        VALUES (?, ?, ?, ?)
        """, (user_id, course_id, 0, completed_topics))
    else:
        # Calculate progress percentage
        if completed_topics >= 10:
            progress = 100
        else:
            progress = completed_topics * 10
        
        # Update user_progress table
        cursor.execute("""
        UPDATE user_progress
        SET progress = ?, completed_topics = ?
        WHERE user_id = ? AND course_id = ?
        """, (progress, completed_topics, user_id, course_id))

# Function to fetch user's enrolled courses
def get_user_courses(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT courses.id, courses.name, COALESCE(user_progress.completed_topics, 0) AS completed_topics
    FROM courses
    LEFT JOIN user_courses ON courses.id = user_courses.course_id AND user_courses.user_id = ?
    LEFT JOIN user_progress ON courses.id = user_progress.course_id AND user_progress.user_id = ?
    """, (user_id, user_id))
    courses = cursor.fetchall()
    conn.close()
    return courses

# Function to render the courses page
def render_courses_page(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    st.title("Courses")
    
    # Fetch user's enrolled courses
    courses = get_user_courses(user_id)

    if not courses:
        st.write("You are not currently enrolled in any courses.")
        st.write("Please register for a course first.")

    for course in courses:
        course_id = course[0]
        course_name = course[1]
        completed_topics = course[2]

        st.header(course_name)
        
        # Get course topics
        topics = get_course_topics(course_id)

        # Display topics and update progress
        completed_topic_flags = []
        for idx, topic in enumerate(topics):
            completed = st.checkbox(topic, key=f"{course_id}_{idx}", value=(idx < completed_topics))
            completed_topic_flags.append(completed)
        
        if st.button(f"Update Progress for {course_name}"):
            completed_topics = sum(completed_topic_flags)
            update_progress(cursor, user_id, course_id, completed_topics)
            conn.commit()
            st.success(f"Progress updated for {course_name}")

    conn.close()


