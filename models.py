import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Description TEXT,
            _is_done BOOLEAN DEFAULT 0,
            _is_deleted BOOLEAN DEFAULT 0,
            CreatedOn DATE DEFAULT CURRENT_DATE,
            DueDate DATE,
            UserId INTEGER REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT,
            CreatedOn DATE DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)

class ToDoModel:
    TABLENAME = "Todo"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, _id):
        query = f"SELECT * FROM {self.TABLENAME} WHERE id={_id}"
        return self.conn.execute(query).fetchone()

    def create(self, params):
        query = f'INSERT INTO {self.TABLENAME} (Title, Description, DueDate, UserId) ' \
                f'VALUES ("{params.get("Title")}", "{params.get("Description")}", "{params.get("DueDate")}", "{params.get("UserId")}")'
        self.conn.execute(query)
        return self.get_by_id(self.conn.lastrowid)

    def update(self, item_id, update_dict):
        set_query = ", ".join([f'{k}="{v}"' for k, v in update_dict.items()])
        query = f"UPDATE {self.TABLENAME} SET {set_query} WHERE id={item_id}"
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} SET _is_deleted=1 WHERE id={item_id}"
        self.conn.execute(query)
        return self.list_items()

    def list_items(self):
        query = f"SELECT * FROM {self.TABLENAME} WHERE _is_deleted=0"
        return [dict(row) for row in self.conn.execute(query).fetchall()]

