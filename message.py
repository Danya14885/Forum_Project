from config import get_connection

def getMessageByChatId(chat_id):
  query = "SELECT * FROM message WHERE chat_id = ?"
  args = [chat_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchall()
  cursor.close()
  connection.close()
  return result

def createMessage(text, datetime, chat_id, sender_id):
  query = "INSERT INTO message (text, datetime, chat_id, sender_id) VALUES (?, ?, ?, ?)"
  args = [text, datetime, chat_id, sender_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  connection.commit()
  cursor.close()
  connection.close()