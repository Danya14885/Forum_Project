var socket = io.connect();
let roomid = document.getElementById('chat_id').innerText;

socket.on('connect', function() {
  var json = {roomid: roomid}
  socket.emit('joined', json)
});

function sendMessage() {
  message = document.getElementById('message').value;
  document.getElementById('message').value = "";

  var date_time = new Date();
  var dateString = date_time.toLocaleString("ru-RU");
  if (message && message != "" && message != "\n") {
    json = {
      message:message,
      date_time:dateString,
    }
    alert(json)
    socket.emit("send", json);

    var el = document.createElement('div');
    el.classList.add('message')
    el.classList.add('right')
    el.innerHTML = `
    <div class="message-header">
        <span class="message-author">Вы</span>
        <span class="message-datetime">${dateString}</span>
    </div>
    <div class="message-text">${message}</div>`;
    var msgholder = document.getElementById("messages-holder")
    msgholder.appendChild(el);
    msgholder.scrollTop = msgholder.scrollHeight;
  }
}

socket.on('broadcast', (response)=> {
  var el = document.createElement('div');
  el.classList.add('message')
  el.classList.add('left')
  el.innerHTML = `<div class="message-header">
        <span class="message-author">${response.sender_email}</span>
        <span class="message-datetime">${response.date_time}</span>
    </div>
    <div class="message-text">${response.text}</div>`
  var msgholder = document.getElementById("messages-holder")
  msgholder.appendChild(el);
  msgholder.scrollTop = msgholder.scrollHeight;
})