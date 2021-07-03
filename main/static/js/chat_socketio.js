document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    const name = document.querySelector('#get-name').innerHTML;
    let room
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user-message').value,
            'name':name, 'room': room});
        document.querySelector('#user-message').value = '';
    };

    socket.on('message', data => {
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br');

            if (data.name == name) {
                p.setAttribute("class", "my-msg");
                span_username.setAttribute("class", "my-name");
                span_username.innerHTML = data.name;

                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerHTML = data.sent_time;
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
                document.querySelector('#display-message-section').append(p);
            }

            else if(typeof data.name !== 'undefined') {
                p.setAttribute("class", "others-msg");
                span_username.setAttribute("class", "others-name");
                span_username.innerHTML = data.name;
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerHTML = data.sent_time;
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
                document.querySelector('#display-message-section').append(p);
            }

            else {
                printSysMsg(data.msg);
            }
        }
        scrollDown();
    });

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML
            if (newRoom === room) {
                msg = `You are already in ${room} room`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });

    function leaveRoom(room) {
        socket.emit('leave', {'name': name, 'room': room});
        document.querySelectorAll('.select-room').forEach(p => {
            p.style.color = "black";
        });
    }

    function joinRoom(room) {
        socket.emit('join', {'name': name, 'room': room});

        document.querySelector('#display-message-section').innerHTML = '';
        document.querySelector("#user-message").focus();
    }

    function scrollDown() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDown()
        document.querySelector("#user-message").focus();
    }

    let msg = document.getElementById("user-message");
    msg.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("send_message").click();
        }
    });
});
