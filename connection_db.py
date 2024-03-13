import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('smart_speaker_ehie.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        password_hash VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create alarms table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        alarm_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        alarm_time DATETIME NOT NULL,
        alarm_message VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

# Create calendar_events table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calendar_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_title VARCHAR(100) NOT NULL,
        event_description TEXT,
        event_datetime DATETIME NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

# Create jokes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jokes (
        joke_id INTEGER PRIMARY KEY AUTOINCREMENT,
        joke_text TEXT NOT NULL,
        category VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Sample data for users table
users_data = [
    ('john_doe', 'john@example.com', 'hashed_password1'),
    ('alice_smith', 'alice@example.com', 'hashed_password2'),
    ('emma_jones', 'emma@example.com', 'hashed_password3'),
    ('michael_brown', 'michael@example.com', 'hashed_password4'),
    ('sophia_wilson', 'sophia@example.com', 'hashed_password5'),
    ('david_clark', 'david@example.com', 'hashed_password6'),
    ('olivia_white', 'olivia@example.com', 'hashed_password7'),
    ('james_taylor', 'james@example.com', 'hashed_password8'),
    ('emily_martin', 'emily@example.com', 'hashed_password9'),
    ('william_anderson', 'william@example.com', 'hashed_password10')
]

# Sample data for alarms table (assigning one alarm to each user)
alarms_data = [
    (1, '08:00', 'Wake up!'),
    (2, '07:30', 'Take medicine'),
    (3, '06:45', 'Morning workout'),
    (4, '09:00', 'Meeting at work'),
    (5, '12:00', 'Lunch time')
]

# Sample data for calendar_events table
calendar_events_data = [
    (1, 'Meeting with client', 'Discuss project details', '2024-03-10 09:00'),
    (2, 'Birthday party', 'Celebrate Alice\'s birthday', '2024-04-15 18:00'),
    (3, 'Team building event', 'Team building activities', '2024-03-20 14:00'),
    (4, 'Conference', 'Tech conference', '2024-05-05 10:00'),
    (5, 'Dentist appointment', 'Regular checkup', '2024-03-25 11:30')
]

# Sample data for jokes table
jokes_data = [
    ('Why did the scarecrow win an award?, Because he was outstanding in his field!', 'Puns'),
    ('Why don’t scientists trust atoms?, Because they make up everything!', 'Science'),
    ('How does a penguin build its house?, Igloos it together!', 'Animals'),
    ('What do you call fake spaghetti?, An impasta!', 'Puns'),
    ('Why did the tomato turn red?, Because it saw the salad dressing!', 'Food')
]

# Insert data into users table
cursor.executemany('''
    INSERT INTO users (username, email, password_hash) 
    VALUES (?, ?, ?)
''', users_data)

# Insert data into alarms table (assigning one alarm to each user)
cursor.executemany('''
    INSERT INTO alarms (user_id, alarm_time, alarm_message) 
    VALUES (?, ?, ?)
''', alarms_data)

# Insert data into calendar_events table
cursor.executemany('''
    INSERT INTO calendar_events (user_id, event_title, event_description, event_datetime) 
    VALUES (?, ?, ?, ?)
''', calendar_events_data)

# Insert data into jokes table
cursor.executemany('''
    INSERT INTO jokes (joke_text, category) 
    VALUES (?, ?)
''', jokes_data)

# Commit changes and close connection
conn.commit()
conn.close()
