var socket = io.connect("/");

var intval = setInterval(function () {
    socket.emit("status", function (data) {
        console.log(data);
    });
}, 5000);