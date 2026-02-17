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
                      name TEXT, 
                      items TEXT, 
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def create_list(self, list_name):
        """Actually saves the list to the database even if it's empty"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Check if it already exists so we don't duplicate
            cursor.execute("SELECT name FROM lists WHERE name = ?", (list_name.lower(),))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO lists (name, items) VALUES (?, ?)", (list_name.lower(), ""))
                conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating list: {e}")
            return False

    def add_item(self, items, list_name):
        # 1. If we got one string like "gas and windows", split it into a list
        if isinstance(items, str):
            # Replace ' and ' with a comma, then split by comma
            # This turns "gas and windows" into ["gas", "windows"]
            items = items.lower().replace(" and ", ",").split(",")
        
        # 2. Clean up each item (remove the word "add" if it's there)
        cleaned_list = []
        for i in items:
            clean = i.strip().replace("add ", "")
            if clean and clean != "and":
                cleaned_list.append(clean)
        
        items_string = ", ".join(cleaned_list)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT items FROM lists WHERE name = ?", (list_name.lower(),))
            result = cursor.fetchone()

            if result:
                existing = result[0]
                updated = (existing + ", " + items_string) if existing else items_string
                cursor.execute("UPDATE lists SET items = ? WHERE name = ?", (updated, list_name.lower()))
                conn.commit()
                # Use the cleaned string for confirmation
                tts(f"Added {items_string} to your {list_name} list.")
            conn.close()
        except Exception as e:
            print(f"Database Error: {e}")

    def read_list(self, list_name):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # We look for the row where 'name' matches what you said
            cursor.execute("SELECT items FROM lists WHERE name = ?", (list_name.lower(),))
            row = cursor.fetchone()
            conn.close()

            if row:
                # row[0] is the string of items (e.g., "apples, bananas")
                tts(f"In your {list_name} list, you have: {row[0]}")
            else:
                tts(f"I couldn't find a list called {list_name}.")
        except Exception as e:
            print(f"Database Error: {e}")

    def view_list(self):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # This gets the 'name' column for every row in the table
            cursor.execute("SELECT name FROM lists")
            rows = cursor.fetchall()
            conn.close()

            if rows:
                tts("You have the following lists:")
                for row in rows:
                    tts(row[0]) # Reads each list name out loud
            else:
                tts("You don't have any lists saved yet.")
        except Exception as e:
            print(f"Database Error: {e}")
