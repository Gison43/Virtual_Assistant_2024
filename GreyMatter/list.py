#/usr/bin/python3
#This is code for a grocery list or any kind of list

import sqlite3
import os
from datetime import datetime
from GreyMatter.SenseCells.tts_engine import tts

# Standardize the database path to match notes.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memory.db")

class List:
    def __init__(self):
        # Ensure the table exists in memory.db
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lists
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          list_name TEXT, 
                          item TEXT, 
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def create_list(self, list_name):
        # In a database, we don't need to create an empty file. 
        # We just confirm the name to the user.
        tts(f"List {list_name} is ready. What would you like to add to it?")

    def add_item(self, items, list_name):
        if isinstance(items, str):
            items = [items]
        
        # Clean the items (remove "and", etc.)
        items = [i.strip() for i in items if i.lower().strip() != "and" and i.strip()]

        try:
            conn = sqlite3.connect(db_path)
            for item in items:
                conn.execute("INSERT INTO lists (list_name, item) VALUES (?, ?)", 
                             (list_name.lower(), item))
            conn.commit()
            conn.close()
            
            tts(f"Added {', '.join(items)} to your {list_name} list.")
            print(f"✅ Saved to DB: {items} in {list_name}")
        except Exception as e:
            print(f"Database Error: {e}")
            tts("I had trouble saving those items to the database.")

    def remove_items(self, item, list_name):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lists WHERE list_name = ? AND item = ?", 
                           (list_name.lower(), item))
            if cursor.rowcount > 0:
                tts(f"Removed {item} from {list_name}.")
            else:
                tts(f"{item} was not found in that list.")
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Error: {e}")

    def read_list(self, list_name):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT item FROM lists WHERE list_name = ?", (list_name.lower(),))
            items = cursor.fetchall()
            conn.close()

            if items:
                tts(f"In your {list_name} list, you have:")
                for row in items:
                    tts(row[0])
            else:
                tts(f"The {list_name} list is currently empty.")
        except Exception as e:
            print(f"Database Error: {e}")

    def view_list(self):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT list_name FROM lists")
            lists = cursor.fetchall()
            conn.close()

            if lists:
                tts("You have the following lists:")
                for lst in lists:
                    tts(lst[0])
            else:
                tts("You don't have any lists saved yet.")
        except Exception as e:
            print(f"Database Error: {e}")
