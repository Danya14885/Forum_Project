from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import datetime
import os
from client_db import getClients, getClientById, getClientByEmail, createClient
from post_db import getPost, getPostById, createPost, deletePostById
from chat_db import getChatWithClientById, getChatBetweenClients, createChat
from message import getMessageByChatId, createMessage
from flask_socketio import SocketIO, join_room


app = Flask(__name__)


io = SocketIO(app)

app.permanent_session_lifetime = datetime.timedelta(days=7)
app.secret_key = 'super secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/static/img'
UPLOAD_FOLDER = APP_ROOT + UPLOAD_FOLD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/static/img/<filename>")
def get_file(filename):
  return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/main', methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
      posts = getPost()
      for i in range(len(posts)):
        client_id = posts[i]["client_id"]
        client_email = getClientById(client_id)["email"]
        posts[i].update({"client_email": client_email})
      return render_template("firstPage.html", posts = reversed(posts))
    elif request.method == "POST":
      date = datetime.date.today().strftime("%d. %m. %Y")
      client_id = session["id"]
      text = request.form["post_text"]
      file = request.files["picture"]
      post_img = file.filename
      print(post_img)
      if post_img != "":
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], post_img))
      createPost(text, post_img, date, client_id)
      allposts = getPost()
      for i in range(len(allposts)):
        client_id = allposts[i]["client_id"]
        client_email = getClientById(client_id)["email"]
        allposts[i].update({"client_email": client_email})
        print("123")
      return render_template("firstPage.html", posts = reversed(allposts))

@app.route('/chatlist/<chat_id>')
def chat(chat_id):
  session["chat_id "] = chat_id
  print('session', session['chat_id'])
  messages = getMessageByChatId(int(chat_id))
    
  for i in range(len(messages)):
    messages[i].update({"sender_email": getClientById(messages[i]["sender_id"])["email"]})
    print('chat', messages)
  return render_template("chat.html", messages=messages, chat_id = chat_id)

@app.route('/chat_list/find_with/<int:client_id>')
def chat_find(client_id):
  print(123)
  current_client_id = session["id"]
  chat = getChatBetweenClients(client_id, current_client_id)
  print(current_client_id, client_id)
  print(chat)
  if chat:
    return redirect(url_for('chat', chat_id = chat["id"]))
  else:
    print(1)
    chat_id = createChat(current_client_id, int(client_id))
    print(chat_id)
    return redirect(url_for('chat', chat_id = chat_id))

@app.route('/chatlist/')
def chat_list():
    client_id = session["id"]
    chats = getChatWithClientById(client_id)
    print(chats)
    if chats == None:
      chats = []
  #Добавление в итоговый список email пользователя (можно отображать просто id)
    for i in range(len(chats)):
        print()
        if chats[i]["first_client_id"] == client_id:
            chats[i].update({"chat_with": getClientById(chats[i]["second_client_id"])["email"]})
        elif chats[i]["second_client_id"] == client_id:
            chats[i].update({"chat_with": getClientById(chats[i]["first_client_id"])["email"]})
    return render_template("chat_list.html", chats=chats)

@app.route('/delete/<post_id>', methods = ["POST"])
def delete(post_id):
  client_id = session["id"]
  post = getPostById(post_id)
  if post["client_id"] == client_id:
    deletePostById(post_id)
    return redirect(url_for("index"))
  
@app.route('/profile/<int:client_id>')
def profile(client_id):
  clientId = client_id
  client = getClientById(clientId)
  print(client)
  return render_template("profile.html", client = client)

@app.route('/', methods = ['GET', 'POST'])
def login():
  if request.method == "POST":
    email = request.form["email"]
    password = request.form["password"]
    print(email, password)
    user_from_db = getClientByEmail(email)
    if not user_from_db:
      return render_template("login.html", error = "Пользователь с такой почтой и паролем не найден")
    else:
      if email == user_from_db['email'] and password == user_from_db['password']:
        session["id"] = user_from_db["id"]
        return redirect(url_for('index'))
      else:
        return render_template("login.html", error = "Неправильный email или пароль")
  elif request.method == "GET":
    return render_template("login.html")
  
@app.route('/signUp/', methods = ['GET', 'POST'])
def signUp():
  if request.method == "POST":
    print("Запрос с методом POST")
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    print(name, email, password)
    user_from_db = getClientByEmail(email)
    if not user_from_db:
      createClient(email, name, password)
      create_client = getClientByEmail(email)
      print(create_client)
      session["id"] = create_client["id"]
      return redirect(url_for('index'))
    else:
      return render_template("signUp.html", error = "Пользователь с таким email уже существует")
  elif request.method == "GET":
    return render_template("signUp.html")

@io.on('send')
def handle_message(json):
  print(json)
  text = json["message"]
  date_time = json["date_time"]
  chat_id = session["chat_id"]
  sender_id = session.get("id")
  createMessage(text, date_time, int(chat_id), sender_id)
  respone = {'text': text,
             'date_time': date_time,
             "sender_email": getClientById(sender_id)["email"]}
  io.emit('broadcast', respone, room = chat_id, include_self = False)

@io.on('joined')
def joined(json):
    print('joinroom', json)
    join_room(json["roomid"])

app.run(host='0.0.0.0', port=81)
