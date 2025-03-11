#/usr/bin/python3
#This is code for a grocery list or any kind of list

import os
from GreyMatter.SenseCells.tts_engine import tts

class List:
    def __init__(self):
        self.items = [] #Initialize the items attribute as an empty list
        self.list_dir = os.path.expanduser("~/GreyMatter/Lists")  #central storage directory
        os.makedirs(self.list_dir, exist_ok=True)

    def _get_file_path(self, list_name):
        """Returns the full path of the list file."""
        return os.path.join(self.list_dir, f"{list_name.replace(' ', '_')}.txt")

    def create_list(self, list_name):
        directory = os.path.expanduser("~/GreyMatter/Lists")
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, f"{list_name.replace(' ', '_')}.txt")
        with open(file_name, 'w') as f:
            for item in self.items:
                f.write(f"{item}\n")
        tts(f"List '{list_name}' has been created and saved")

    def add_item(self,item, list_name):
        file_path = self._get_file_path(list_name)
        #load existing items from file
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                self.items = [line.strip() for line in f.readlines()]
                #add new item and save
        self.items.append(item)
        self.save_list(list_name)
        print(f"{item} added to the list called {list_name}")

    def save_list(self, list_name):
        directory = os.path.expanduser("~/GreyMatter/Lists")
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, f"{list_name.replace(' ', '_')}.txt")
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
        directory = os.path.expanduser("~/GreyMatter/Lists")
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, f"{list_name.replace(' ', '_')}.txt")
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
