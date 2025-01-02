import sqlite3

def init_db():
    with sqlite3.connect("chat_history.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                model_name TEXT,
                user_message TEXT,
                model_response TEXT
            )
        """)
        conn.commit()

def save_chat(session_id, model_name, user_message, model_response):
    with sqlite3.connect("chat_history.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (session_id, model_name, user_message, model_response)
            VALUES (?, ?, ?, ?)
        """, (session_id, model_name, user_message, model_response))
        conn.commit()
        
def load_chat(session_id=None):
    with sqlite3.connect("chat_history.db") as conn:
        cursor = conn.cursor()
        
        # 如果 session_id 为 None，加载所有会话记录
        if session_id is None:
            cursor.execute("""
                SELECT session_id, timestamp, user_message, model_response
                FROM chat_history
                ORDER BY timestamp ASC
            """)
        else:
            cursor.execute("""
                SELECT timestamp, model_name, user_message, model_response
                FROM chat_history WHERE session_id = ?
                ORDER BY timestamp ASC
            """, (session_id,))
        
        rows = cursor.fetchall()

    # 如果 session_id 是 None，我们将返回每个会话的 session_id 和相关信息
    if session_id is None:
        return [{"session_id": row[0], "timestamp": row[1], "user_message": row[2], "model_response": row[3]} for row in rows]
    
    # 否则，返回指定会话的详细信息
    return [{"timestamp": row[0], "model_name": row[1], "user_message": row[2], "model_response": row[3]} for row in rows]

if __name__ == "__main__":
    init_db()
    # 
    # 测试保存聊天记录
    session_id = "session123"
    model_name = "TestModel"
    user_message = "Hello, how are you?"
    model_response = "I'm just a machine, but thanks for asking!s"
    save_chat(session_id, model_name, user_message, model_response)
    
    #测试加载聊天记录
    chats = load_chat(None)
    for chat in chats:
        print(chat)