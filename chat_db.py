from config import get_connection


def getChatWithClientById(id):
  query = "SELECT * FROM chat WHERE first_client_id = ? or second_client_id = ?"
  args = [id, id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchall()
  cursor.close()
  connection.close()
  return result


def getChatBetweenClients(first_client_id, second_client_id):
  query = "SELECT * FROM chat WHERE first_client_id = ? and second_client_id = ? or second_client_id = ? and first_client_id = ?"
  args = [first_client_id, second_client_id, first_client_id, second_client_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchone()
  cursor.close()
  connection.close()
  return result


def createChat(first_client_id, second_client_id):
  query = "INSERT INTO chat (first_client_id, second_client_id) VALUES (?, ?)"
  args = [first_client_id, second_client_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  connection.commit()
  cursor.close()
  connection.close()
  return cursor.lastrowid
