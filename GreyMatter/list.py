#/usr/bin/python3
#This is code for a grocery list or any kind of list

import os
from user_input import get_user_input
from GreyMatter.SenseCells.tts_engine import tts

class List:
    def __init(self):
        self.items = []

    def create_list(self):
        tts("Sure.  Let's create a new list.")
        tts("What would you like to name your new list?")
        list_name = get_user_input()
        items = []
        while True:
           item = tts("What would you like to add to the list? Say done when finished.")
           if user_input == 'done':
              break
           items.append(item)
        self.save_list(list_name, items)

    def save_list(self, list_name, items):
        file_name = f"{list_name}.txt"
        with open(file_name, 'w') as f:
            for item in items:
                f.write(f"{item}\n")
        tts(f"List '{list_name}' has been created and saved")

    def add_item(self,item):
        self.items.append(item)
        print(f"{item} added to the list called {list_name}")

    def remove_items(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} removed from the list called {list_name}")
        else:
            print(f"{item} is not in the list called {list_name}")

    def read_list(self, list_name):
        file_name = f"{list_name}.txt"
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                items = f.readlines()
            tts(f"Here are the items in list called '{list_name}':")
            for item in items:
                tts(item.strip())
        else:
            tts(f"Sorry list '{list_name}' does not exist.")

    def view_list(self):
        if self.items:
            print("{list_name}"
            for index, item in enumerate(self.items, start = 1):
            print(f"{index}. {item}")
        else:
            print(f"Your list called {list_name} is empty.")
