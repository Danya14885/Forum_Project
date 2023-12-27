import sqlite3


#Получение соединения
def get_connection():
  connection = sqlite3.connect("db/chat.db")
  connection.row_factory = dict_factory  #Специальный параметр для получения данных в виде словаря
  return connection


#Пользовательская настройка для формирования словаря
def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d