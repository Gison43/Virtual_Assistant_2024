#/usr/bin/python3
#This is code for a grocery list or any kind of list

import sqlite3
import os
from datetime import datetime
from GreyMatter.SenseCells.tts_engine import tts

# Standardized path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

class List:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS lists
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      list_name TEXT, 
                      item TEXT, 
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def create_list(self, list_name):
        # We don't need to create a file, the table handles it.
        # This just confirms the name to the user.
        return True 

    def add_item(self, items, list_name):
        if isinstance(items, str):
            items = [items]
        
        # Clean the items
        items = [i.strip() for i in items if i.lower().strip() != "and" and i.strip()]

        conn = sqlite3.connect(db_path)
        for item in items:
            conn.execute("INSERT INTO lists (list_name, item) VALUES (?, ?)", 
                         (list_name.lower(), item))
        conn.commit()
        conn.close()
        tts(f"Added {', '.join(items)} to your {list_name} list.")
