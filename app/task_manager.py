import sqlite3
from datetime import datetime

class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            category TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, task, category):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO tasks (task, category, created_at) VALUES (?, ?, ?);"
        self.conn.execute(query, (task, category, now))
        self.conn.commit()

    def get_all_tasks(self):
        return self.conn.execute("SELECT * FROM tasks").fetchall()

    def mark_done(self, task_id):
        self.conn.execute("UPDATE tasks SET status='done' WHERE id=?;", (task_id,))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id=?;", (task_id,))
        self.conn.commit()

    def edit_task(self, task_id, new_text=None, new_category=None):
        if new_text:
            self.conn.execute("UPDATE tasks SET task=? WHERE id=?;", (new_text, task_id))
        if new_category:
            self.conn.execute("UPDATE tasks SET category=? WHERE id=?;", (new_category, task_id))
        self.conn.commit()
        
    def delete_completed_tasks(self):
        self.conn.execute("DELETE FROM tasks WHERE status = 'done';")
        self.conn.commit()

    def search_tasks(self, keyword):
        query = "SELECT * FROM tasks WHERE task LIKE ? OR category LIKE ?"
        like_pattern = f"%{keyword}%"
        return self.conn.execute(query, (like_pattern, like_pattern)).fetchall()

