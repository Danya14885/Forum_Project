from config import get_connection

def getPost():
  query = "SELECT * FROM post"
  connection = get_connection()
  cursor = connection.execute(query)
  result = cursor.fetchall()
  cursor.close()
  connection.close()
  return result
  
def getPostById(id):
  query = "SELECT * FROM post WHERE id = ?"
  args = [id]  
  connection = get_connection()
  cursor = connection.execute(query, args)
  result = cursor.fetchone()
  cursor.close()
  connection.close()
  return result
  
def createPost(text, post_img, date, client_id):
  query = "INSERT INTO post (text, post_img, date, client_id) VALUES (?, ?, ?, ?)"
  args = [text, post_img, date, client_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  connection.commit()
  cursor.close()
  connection.close()

def deletePostById(post_id):
  query = "DELETE FROM post WHERE id = ?"
  args = [post_id]
  connection = get_connection()
  cursor = connection.execute(query, args)
  connection.commit()
  cursor.close()
  connection.close()
  