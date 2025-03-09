import sqlite3

def add_words(conn, spanish):
#inserts a new row into the  table statement
  sql = ''' INSERT INTO spanish(spanish_word, english_word)
    VALUES(?,?) '''  

#create a cursor
  cursor = conn.cursor()

#execute the INSERT statement
  cursor.execute(sql, spanish)

#commit the changes
  conn.commit()

#get teh id of the last inserted row
  return cursor.lastrowid

def main():
  try:
    with sqlite3.connect("spanish_words.db") as conn:  #open a connection to the database

    #add spanish/english words
    spanish = [
      ('toalla', 'towel'),
      ('rusia', 'russia'),
      ('bolsos', 'purses'),
      ('botas', 'boots'),
      ('cuero', 'leather'),
      ('abotanaré', 'to button up'),
      ('un barba', 'a beard'),
      ('desodorante, 'deodorant'),
      ('un anillo', 'a ring'),
      ('un bigote', 'a moustache')
      ('planchar', 'to iron'),
      ('maqillar', 'to put on makeup')
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
      ('pulseras', bracelets'),
      ('pelo rizado', 'curly hair'),
      ('abotanaré', 'to button up'),
      ('poner', 'to put on'),
      ('guantes', 'gloves'),
      ('calcetines', 'socks'),
    ]

    for spanish in spanishs:
      spanish_list = add_words(conn, spanish)
      print(f'Created spanish list with the id{spanish_list}')

  except sqlite3.Error as e:
    print(e)
