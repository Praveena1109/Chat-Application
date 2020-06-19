document.addEventListener('DOMContentLoaded', () => {

var socket = io.conect(location.protocol + '//' + document.domain + ':' + location.port);

const name = document.querySelector('#get-username').innerHTML;

document.querySelector('#sendButton').onclick = () => {
  socket.emit('incoming-msg', {'msg': document.querySelector('#input_msg').value,
              'username': name});

          document.querySelector('#input_msg').value = '';
      };
});

socket.on('message', data => {
  // Display current message
  if (data.msg) {
      const p = document.createElement('p');
      const span_username = document.createElement('span');
      const span_timestamp = document.createElement('span')
      const br = document.createElement('br')
      // Display user's own message
      if (data.username == name) {
          p.setAttribute("class", "my-msg");
          // Username
          span_username.setAttribute("class", "my-username");
          span_username.innerText = data.username;
          // Timestamp
          span_timestamp.setAttribute("class", "timestamp");
          span_timestamp.innerText = data.time_stamp;
          // HTML to append
          p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML
          //Append
          document.querySelector('#display-message-section').append(p);
      }
      // Display other users' messages
      else if (typeof data.username !== 'undefined') {
          p.setAttribute("class", "others-msg");
          // Username
          span_username.setAttribute("class", "other-username");
          span_username.innerText = data.username;
          // Timestamp
          span_timestamp.setAttribute("class", "timestamp");
          span_timestamp.innerText = data.time_stamp;
          // HTML to append
          p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
          //Append
          document.querySelector('#display-message-section').append(p);
      }
      // Display system message
      else {
          printSysMsg(data.msg);
      }


  }
  scrollDownChatWindow();
});

// Scroll chat window down
function scrollDownChatWindow() {
  const chatWindow = document.querySelector("#display-message-section");
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Print system messages
function printSysMsg(msg) {
  const p = document.createElement('p');
  p.setAttribute("class", "system-msg");
  p.innerHTML = msg;
  document.querySelector('#display-message-section').append(p);
  scrollDownChatWindow()

  // Autofocus on text box
  document.querySelector("#user_message").focus();
}
