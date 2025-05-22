# 2. Файл database.py
import sqlite3
from contextlib import closing

DATABASE_NAME = 'dating.db'

def init_db():
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        
        # Пересоздаем таблицу users с правильными столбцами
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            city TEXT NOT NULL,
            bio TEXT NOT NULL,
            media TEXT NOT NULL,
            media_type TEXT NOT NULL,  
            preferences TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS likes (
            like_id INTEGER PRIMARY KEY AUTOINCREMENT,
            liker_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(liker_id) REFERENCES users(user_id),
            FOREIGN KEY(target_id) REFERENCES users(user_id)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS like_messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            like_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY(like_id) REFERENCES likes(like_id)
        )''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_profiles_city_age 
          ON profiles(city, age)''')
        
        conn.commit()

def add_user(user_id, username, full_name):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', 
                 (user_id, username, full_name))
        conn.commit()

def save_profile(user_id, profile_data):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO profiles 
                  (user_id, name, age, gender, city, bio, media, preferences)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, 
                   profile_data['name'],
                   profile_data['age'],
                   profile_data['gender'],
                   profile_data['city'],
                   profile_data['bio'],
                   profile_data['media'],
                   profile_data['preferences']))
        conn.commit()

def get_profile(user_id):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,))
        return c.fetchone()

def get_random_profile(current_user_id: int, current_preferences: str):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        
        # Формируем условия для фильтрации
        query = '''
            SELECT * FROM profiles 
            WHERE user_id != ?
            AND gender = ?
        '''
        params = (current_user_id, current_preferences)

        # Если предпочтения "any" - убираем фильтр по полу
        if current_preferences.lower() == 'any':
            query = '''
                SELECT * FROM profiles 
                WHERE user_id != ?
            '''
            params = (current_user_id,)

        c.execute(query + ' ORDER BY RANDOM() LIMIT 1', params)
        return c.fetchone()

def get_likes_with_messages(target_id):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('''SELECT l.liker_id, u.full_name, lm.message 
                  FROM likes l
                  LEFT JOIN like_messages lm ON l.like_id = lm.like_id
                  JOIN users u ON l.liker_id = u.user_id
                  WHERE l.target_id = ?''', (target_id,))
        return c.fetchall()

# Остальные функции остаются без изменений


def add_user(user_id, username, full_name):  #dobov us
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?)', 
                 (user_id, username, full_name))
        conn.commit()

def save_profile(user_id, profile_data): #soh anketi
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO profiles 
                  (user_id, name, age, gender, city, bio, media, preferences)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, *profile_data.values()))
        conn.commit()

def get_profile(user_id): 
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id,))
        return c.fetchone()



def add_like(liker_id, target_id):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO likes (liker_id, target_id) VALUES (?, ?)',
                 (liker_id, target_id))
        conn.commit()

def check_match(liker_id, target_id):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('''SELECT 1 FROM likes 
                  WHERE liker_id = ? AND target_id = ?''',
                 (target_id, liker_id))
        return c.fetchone() is not None

def add_match(user1_id, user2_id):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO matches (user1_id, user2_id) VALUES (?, ?)',
                 (user1_id, user2_id))
        conn.commit()

