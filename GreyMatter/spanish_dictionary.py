#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('spanish_words.db')
print("Opened database successfully")

conn.execute("""CREATE TABLE IF NOT EXISTS spanish_words 
  (spanish_word text NOT NULL,
  english_word text NOT NULL);""")

print ("Table created successfully");

conn.commit()
conn.close()

def add_words(conn, spanish):
#inserts a new row into the  table statement
  sql = ''' INSERT INTO spanish_words(spanish_word, english_word)
    VALUES(?,?) '''  

#create a cursor
  cursor = conn.cursor()

#execute the INSERT statement
  cursor.execute(sql, spanish)

#commit the changes
  conn.commit()

#get the id of the last inserted row
  return cursor.lastrowid

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
        ('abotanaré', 'to button up'),
        ('un barba', 'a beard'),
        ('desodorante', 'deodorant'),
        ('un anillo', 'a ring'),
        ('un bigote', 'a moustache'),
        ('planchar', 'to iron'),
        ('maqillar', 'to put on makeup'),
        ('mejórante pronto', 'get well soon'),
        ('violines','violins'),
        ('bosos', 'purses'),
        ('doblar', 'to fold'),
        ('acoser', 'to sew'),
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
    ]

    for spanish in spanishs:
      spanish_list = add_words(conn, spanish)
      print(f'Created spanish list with the id {spanish_list}')

  except sqlite3.Error as e:
    print(e)

if __name__ == '__main__':
  main()
