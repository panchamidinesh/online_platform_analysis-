import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        user_id INTEGER,
        course_id INTEGER,
        progress INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(course_id) REFERENCES courses(id),
        PRIMARY KEY(user_id, course_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_courses (
        user_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(course_id) REFERENCES courses(id),
        PRIMARY KEY(user_id, course_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        question TEXT NOT NULL,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        correct_option INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_scores (
        user_id INTEGER,
        quiz_id INTEGER,
        score INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id),
      PRIMARY KEY(user_id, quiz_id)
    )
    ''')

    # Insert sample users
    users = [
        ('santosh', 'password1'),
        ('Priya', 'password2'),
        ('Raj', 'password3'),
        ('Sneha', 'password4'),
        ('Vikram', 'password5'),
        ('Aditi', 'password6'),
    ]
    cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)

    # Insert sample courses
    courses = [
        ('Machine Learning',),
        ('Python Programming',),
        ('Data Structures',),
        ('Web Development',),
        ('Database Systems',)
    ]
    cursor.executemany("INSERT INTO courses (name) VALUES (?)", courses)

    # Insert sample user progress
    user_progress = [
        (1, 1, 50),
        (1, 2, 75),
        (2, 1, 60),
        (2, 3, 80),
        (3, 4, 40),
        (3, 5, 90),
        (4, 1, 70),
        (4, 2, 85),
        (5, 3, 55),
        (5, 4, 65),
        (6, 5, 95),
    ]
    cursor.executemany("INSERT INTO user_progress (user_id, course_id, progress) VALUES (?, ?, ?)", user_progress)

    # Insert sample quizzes with options and correct answers
    quizzes = [
        # Machine Learning
        (1, 'What is supervised learning?', 'A type of machine learning', 'A type of unsupervised learning', 'A type of reinforcement learning', 'A type of semi-supervised learning', 1),
        (1, 'Name an algorithm used in supervised learning.', 'Decision Tree', 'Naive Bayes', 'K-Means', 'Random Forest', 1),
        (1, 'What is unsupervised learning?', 'A type of machine learning', 'A type of reinforcement learning', 'A type of supervised learning', 'A type of semi-supervised learning', 1),
        (1, 'Name an algorithm used in unsupervised learning.', 'K-Means', 'Decision Tree', 'Naive Bayes', 'Random Forest', 1),
        (1, 'What is a neural network?', 'A series of algorithms that mimic the operations of a human brain', 'A type of database system', 'A type of programming language', 'A type of web development tool', 1),

        # Python Programming
        (2, 'What is a list?', '[1, 2, 3]', 'A collection of elements', 'A type of tuple', 'A type of dictionary', 2),
        (2, 'How do you declare a list in Python?', '[1, 2, 3]', '[1, 2, 3, 4]', '[1, 2]', '[1, 2, 3, 4, 5]', 1),
        (2, 'What is a dictionary?', 'A collection of key-value pairs', 'A type of list', 'A type of tuple', 'A type of function', 1),
        (2, 'How do you declare a dictionary in Python?', '{"key": "value"}', '{"item": "element"}', '{"name": "data"}', '{"value": "key"}', 1),
        (2, 'What is a function?', 'A block of code which only runs when it is called', 'A type of loop', 'A type of list', 'A type of dictionary', 1),

        # Data Structures
        (3, 'What is a binary tree?', 'A tree with two children', 'A data structure used in AI', 'A type of sorting algorithm', 'A way to store data in Python', 1),
        (3, 'Define a linked list.', 'A sequence of nodes', 'A type of database system', 'A type of web development tool', 'A type of machine learning', 1),
        (3, 'What is a stack?', 'A linear data structure which follows the LIFO principle', 'A type of loop', 'A type of list', 'A type of dictionary', 1),
        (3, 'What is a queue?', 'A linear data structure which follows the FIFO principle', 'A type of database system', 'A type of web development tool', 'A type of machine learning', 1),
        (3, 'What is a graph?', 'A collection of nodes connected by edges', 'A type of sorting algorithm', 'A way to store data in Python', 'A type of machine learning', 1),

        # Web Development
        (4, 'What is HTML?', 'HyperText Markup Language', 'A programming language', 'A database system', 'A type of operating system', 1),
        (4, 'What is CSS used for?', 'Styling web pages', 'Programming language', 'Database management', 'Operating system', 1),
        (4, 'What is JavaScript?', 'A programming language used to create interactive effects within web browsers', 'A type of sorting algorithm', 'A way to store data in Python', 'A type of machine learning', 1),
        (4, 'What is a framework?', 'A platform for developing software applications', 'A type of loop', 'A type of list', 'A type of dictionary', 1),
        (4, 'Name a popular web development framework.', 'React', 'Vue', 'Angular', 'Django', 1),

        # Database Systems
        (5, 'What is SQL?', 'Structured Query Language', 'A programming language', 'A scripting language', 'A markup language', 1),
        (5, 'What is normalization?', 'Reducing redundancy', 'A type of loop', 'A type of list', 'A type of dictionary', 1),
        (5, 'What is a primary key?', 'A unique identifier for a record in a table', 'A type of database system', 'A type of web development tool', 'A type of machine learning', 1),
        (5, 'What is a foreign key?', 'A field in one table that uniquely identifies a row of another table', 'A type of sorting algorithm', 'A way to store data in Python', 'A type of machine learning', 1),
        (5, 'What is a join operation?', 'Combining columns from two or more tables based on a related column', 'A type of database system', 'A type of web development tool', 'A type of machine learning', 1),
    ]
    cursor.executemany("INSERT INTO quizzes (course_id, question, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)", quizzes)

    # Insert sample user course enrollments
    user_courses = [
        (1, 1),  # Santosh enrolled in Machine Learning
        (1, 2),  # Santosh enrolled in Python Programming
        (2, 1),  # Priya enrolled in Machine Learning
        (2, 3),  # Priya enrolled in Data Structures
        (3, 4),  # Raj enrolled in Web Development
        (3, 5),  # Raj enrolled in Database Systems
        (4, 1),  # Sneha enrolled in Machine Learning
        (4, 2),  # Sneha enrolled in Python Programming
        (5, 3),  # Vikram enrolled in Data Structures
        (5, 4),  # Vikram enrolled in Web Development
        (6, 5),  # Aditi enrolled in Database Systems
    ]
    cursor.executemany("INSERT INTO user_courses (user_id, course_id) VALUES (?, ?)", user_courses)

    # Insert sample quiz scores
    # quiz_scores = [
    #     (1, 1, 4),  # Santosh scored 4 out of 5 in Machine Learning Quiz 1
    #     (1, 2, 3),  # Santosh scored 3 out of 5 in Python Programming Quiz 1
    #     (2, 1, 5),  # Priya scored 5 out of 5 in Machine Learning Quiz 1
    #     (2, 3, 4),  # Priya scored 4 out of 5 in Data Structures Quiz 1
    #     (3, 4, 3),  # Raj scored 3 out of 5 in Web Development Quiz 1
    #     (3, 5, 4),  # Raj scored 4 out of 5 in Database Systems Quiz 1
    #     (4, 1, 5),  # Sneha scored 5 out of 5 in Machine Learning Quiz 1
    #     (4, 2, 4),  # Sneha scored 4 out of 5 in Python Programming Quiz 1
    #     (5, 3, 5),  # Vikram scored 5 out of 5 in Data Structures Quiz 1
    #     (5, 4, 3),  # Vikram scored 3 out of 5 in Web Development Quiz 1
    #     (6, 5, 4),  # Aditi scored 4 out of 5 in Database Systems Quiz 1
    # ]
    # cursor.executemany("INSERT INTO quiz_scores (user_id, quiz_id, score) VALUES (?, ?, ?)", quiz_scores)

    cursor.execute('ALTER TABLE user_progress ADD COLUMN completed_topics INTEGER DEFAULT 0;');

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
