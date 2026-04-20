import sqlite3

def init_db():
    conn = sqlite3.connect("xsos_final.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS songs (vid_id TEXT PRIMARY KEY, file_id TEXT, title TEXT)")
    conn.commit()
    conn.close()

def check_song(vid_id):
    conn = sqlite3.connect("xsos_final.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id, title FROM songs WHERE vid_id=?", (vid_id,))
    res = cursor.fetchone()
    conn.close()
    return res

def save_song(vid_id, file_id, title):
    conn = sqlite3.connect("xsos_final.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO songs VALUES (?, ?, ?)", (vid_id, file_id, title))
    conn.commit()
    conn.close()

    def get_users_count():
        conn = sqlite3.connect("xsos_final.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def get_all_users():
        conn = sqlite3.connect("xsos_final.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()
        conn.close()
        return users