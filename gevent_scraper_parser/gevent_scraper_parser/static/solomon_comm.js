WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

// socket.io specific code
var socket = io.connect('http://' + window.location.hostname + ':8000/solomon_comm');

socket.on('connect', function () {
    
});

// socket.on('nickname', function (msg) {
//     $('#nickname').append($('<p>').append($('<em>').text(msg)));
// });

// socket.on('announcement', function (msg) {
//     $('#lines').append($('<p>').append($('<em>').text(msg)));
// });

// socket.on('nicknames', function (nicknames) {
//     $('#nicknames').empty();
//     for (var i in nicknames) {
//         $('#nicknames').append($('<li>').text(nicknames[i]));
//     }
// });

socket.on('msg_to_user', function(a) {
    console.log(a);
    $('#messages').append($('<pre>').append($('<code>').append(a)));
    $("#loading").hide();
});

// socket.on('reconnect', function () {
//     $('#lines').remove();
//     message('System', 'Reconnected to the server');
// });

// socket.on('need_reconnect', function () {
//     window.location="/";
// });

// socket.on('reconnecting', function () {
//     message('System', 'Attempting to re-connect to the server');
// });

// socket.on('error', function (e) {
//     message('System', e ? e : 'A unknown error occurred');
// });


// send message
$(function () {
    $('#send').click(function () {
        $("#loading").show();
        socket.emit('url',{url: $('#url').val(), webpage: $('#type').val()});
        return false;
    });

    function clear () {
        $('#message').val('').focus();
    };
});
