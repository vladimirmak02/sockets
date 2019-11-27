$('#loginBtn').on('click', _ => {
    if (window.screen.height * window.devicePixelRatio > 1000){
        $(chat).css('height', '800px')
    }
    else{
        $(chat).css('height', window.screen.height * window.devicePixelRatio-400+'px')
    }
    $("#sendMessageContent").show();
    $("#loginBtn").attr("disabled", "disabled");
    $("#login").attr("disabled", "disabled");
    $("#loginContainer").css("display","none");
    $('#message').focus();
    let socket = io.connect("http://10.0.0.39:5000/chat");

    socket.on('response', msg => {
        $("#chat").append('(' + msg['time'] + ") " + msg['login'] + ': ' + msg['data'] + '<br/>');
        let chatDiv = document.querySelector('#chat');
        chatDiv.scrollTop = chatDiv.scrollHeight;
    });

    socket.on('connect', _ => {
        socket.emit('newUser', {"login": $('#login').val()});
    });


    $('#send').on('click', _ => {
        console.log('CLICK')
        let msg = $('#message').val();
        socket.emit("newMsg", {'login': $('#login').val(), 'message': msg});
        $('#message').val('');
    });
});

$(document).ready(function(){
    $('#login').focus();
});

$("#message").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $('#send').click();
    }
});
$("#login").on('keyup', function (e) {
    if (e.keyCode == 13) {
        $('#loginBtn').click();
    }
});
//TODO : Bootstrap pretty