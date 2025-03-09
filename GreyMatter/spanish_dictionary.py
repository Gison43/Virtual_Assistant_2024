#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('spanish_words.db')
print("Opened database successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS spanish_words
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  spanish_word TEXT NOT NULL,
  english_word TEXT NOT NULL);""")

print ("Table created successfully")

conn.commit()
conn.close()

def add_words(conn, spanish):
#inserts a new row into the  table statement
  sql = ''' INSERT INTO spanish_words(spanish_word, english_word)
    VALUES(?,?) '''  
  try:  
    cursor = conn.cursor() #create a cursor
    cursor.execute(sql, spanish) #execute the INSERT statement
    conn.commit() #commit the changes
    return cursor.lastrowid #get the id of the last inserted row
  except: sqlite3.Error as e:
    print(f"Error inserting {spanish}: {e}")
    return None #return None if insertion failes

def main():
  try:
    with sqlite3.connect('spanish_words.db') as conn:  #open a connection to the database

    #add spanish/english words
      spanishs = [
        ('toalla', 'towel'),
        ('rusia', 'russia'),
        ('bolsos', 'purses'),
        ('botas', 'boots'),
        ('cuero', 'leather'),
        ('un barba', 'a beard'),
        ('desodorante', 'deodorant'),
        ('un anillo', 'a ring'),
        ('un bigote', 'a moustache'),
        ('planchar', 'to iron'),
        ('maquillar', 'to put on makeup'),
        ('mejórante pronto', 'get well soon'),
        ('violines','violins'),
        ('bolsos', 'purses'),
        ('coser', 'to sew'),
        ('bolsillos', 'pockets'),
        ('bufanda', 'scarf'),
        ('saco', 'suit jacket'),
        ('abrigo', 'jacket'),
        ('llàmeme', 'call me'),
        ('salud', 'bless you'),
        ('fiebre', 'fever'),
        ('pulseras', 'bracelets'),
        ('pelo rizado', 'curly hair'),
        ('abotanaré', 'to button up'),
        ('poner', 'to put on'),
        ('cretes', 'earrings'),
        ('abotonar', 'to button up'),
        ('collar', 'necklace'),
        ('doblar', 'to fold'),
        ('se quita', 'to take off'),
        ('cremallera', 'zipper'),
        ('guantes', 'gloves'),
        ('calcetines', 'socks'),
        ('largo', 'long'),
        ('carne de vaca', 'beef'),
        ('horno', 'oven'),
        ('corto', 'short'),
        ('cierra la cremallera', 'close the zipper'),
        ('papas hervidas', 'boiled potatoes'),
        ('vegetariano', 'vegeterian'),
        ('sartén', 'frying pan'),
        ('cebollas fritas', 'fried onion rings'),
        ('huevos hervidos', 'boiled eggs'),
        ('sección', 'section'),
        ('ten cuidado', 'be careful'),
    ]

      for spanish in spanishs:
        spanish_list = add_words(conn, spanish)
        if spanish_list:
          print(f'Created spanish list with the id {spanish_list}')
        else:
          print(f"Skipping duplicate or error for {spanish_list}")

  except sqlite3.Error as e:
    print(e)

if __name__ == '__main__':
  main()
