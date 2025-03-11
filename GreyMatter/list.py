#/usr/bin/python3
#This is code for a grocery list or any kind of list

import os
from GreyMatter.SenseCells.tts_engine import tts

class List:
    def __init__(self):
        self.list_dir = os.path.expanduser("~/Virtual_Assistant_2024/GreyMatter/Lists")  #central storage directory
        os.makedirs(self.list_dir, exist_ok=True)

    def _get_file_path(self, list_name):
        """Returns the full path of the list file."""
        return os.path.join(self.list_dir, f"{list_name.replace(' ', '_')}.txt")

    def create_list(self, list_name):
        file_name = self._get_file_path(list_name)
        with open(file_name, 'w') as f:
            f.write("") #ensure the file is properly initialized
        tts(f"List '{list_name}' has been created and saved in {self.list_dir}")
        print(f"Saving list to: {file_name}")  #debugging
        if os.path.exists(file_name):
            print(f"✅ List file created at: {file_name}")
        else:
            print(f"❌ ERROR: List file was NOT created at: {file_name}")


    def add_item(self,item, list_name):
        file_path = self._get_file_path(list_name)
        #load existing items from file

        items = []  #initialize the list before checking the file
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                items = [line.strip() for line in f.readlines()]
                
        items.append(item)
        #add new item and save
        with open(file_path, 'w') as f:
            for i in items:
                f.write(f"{i}\n")
        print(f"{item} added to the list called {list_name}")
        tts(f"{item} added to the list called {list_name}")

    def save_list(self, list_name):
        directory = os.path.expanduser("~/GreyMatter/Lists")
        os.makedirs(directory, exist_ok=True)
        file_name = os.path.join(directory, f"{list_name.replace(' ', '_')}.txt")

        items = []
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                items = [line.strip() for line in f.readlines()]
    #write the items back to the file
        with open(file_name, 'a') as f:
            for item in items:
                f.write(f"{item}\n")
                
        if os.path.exists(file_name):
            print(f"List successfully saved at: {file_name}")

        else:
            print(f"ERROR: List was not saved at: {file_name}")

    def remove_items(self, item, list_name):
        file_path = self._get_file_path(list_name)

        if not os.path.exists(file_path):
            tts(f"Sorry, the list '{list_name}' does not exist.")
            return

        with open(file_path, 'r') as f:
            items = [line.strip() for line in f.readlines()]
            
        if item in items:
            items.remove(item)
            with open(file_path, 'w') as f:
                for i in items:
                    f.write(f"{i}\n")
            tts(f"{item} removed from the list called {list_name}")
            print(f"{item} removed from the list called {list_name}")
        else:
            print(f"{item} is not in the list called {list_name}")
            tts(f"{item} is not in the list called {list_name}")

    def read_list(self, list_name):
        file_path = self._get_file_path(list_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                items = [line.strip() for line in f.readlines()]

            if items:
                tts(f"Here are the items in the list called '{list_name}':")
                for item in items:
                    tts(item)
            else:
                tts(f"The list called '{list_name}' is empty")
        else:
            tts(f"Sorry the list called '{list_name}' does not exist")
            
    def view_list(self):
        lists = os.listdir(self.list_dir)
        
        if lists:
            tts("Here are your available lists:")
            for lst in lists:
                list_name = lst.replace("_", " ").replace(".txt"," ")
                tts(list_name)
