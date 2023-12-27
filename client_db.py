from config import get_connection

def getClients():
  query = "SELECT * FROM client"
  connection = get_connection()
  cursor = connection.execute(query)
  result = cursor.fetchall()
  cursor.close()
  connection.close()
  return result
  
def getClientById(id):
  query = "SELECT * FROM client WHERE id = ?"
  args = [id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchone()
  cursor.close()
  connection.close()
  return result
  
def getClientByEmail(email):
  query = "SELECT * FROM client WHERE email = ?"
  args = [email]
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchone()
  cursor.close()
  connection.close()
  return result
  
def createClient(email, name, password):
  query = "INSERT INTO client (email, name, password) VALUES (?, ?, ?)"
  args = [email, name, password]
  connection = get_connection()
  cursor = connection.execute(query, args)
  connection.commit()
  cursor.close()
  connection.close()
  
  
  