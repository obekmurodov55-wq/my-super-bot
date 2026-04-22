import sqlite3

def add_user(user_id, username, first_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)', 
                   (user_id, username, first_name))
    conn.commit()
    conn.close()
