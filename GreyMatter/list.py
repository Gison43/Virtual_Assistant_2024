#/usr/bin/python3
#This is code for a grocery list or any kind of list

import os
from GreyMatter.SenseCells.tts_engine import tts

class List:
    def __init__(self):
        self.items = [] #Initialize the items attribute as an empty list

    def create_list(self, list_name):
        file_name = f"{list_name.replace(' ', '_')}.txt"
        with open(file_name, 'w') as f:
            for item in self.items:
                f.write(f"{item}\n")
        tts(f"List '{list_name}' has been created and saved")

    def add_item(self,item, list_name):
        self.items.append(item)
        self.save_list(list_name)
        print(f"{item} added to the list called {list_name}")

    def save_list(self, list_name):
        file_name = f"{list_name.replace(' ', '_')}.txt"
        with open(file_name, 'w') as f:
            for item in self.items:
                f.write(f"{item}\n")

    def remove_items(self, item, list_name):
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
            if items:
                tts(f"Here are the items in list called '{list_name}':")
            for item in items:
                tts(item.strip())
            else:
                tts(f"The list called '{list_name}' is empty")
        else:
            tts(f"Sorry the list called '{list_name}' does not exist.")

    def view_list(self):
        if self.items:
            print("{list_name}")
            for index, item in enumerate(self.items, start = 1):
                print(f"{index}. {item}")
        else:
            print(f"Your list called {list_name} is empty.")
