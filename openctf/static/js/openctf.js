var socket = io.connect("/");

var loop = function () {
    socket.emit("status", function (data) {
        data = JSON.parse(data);
        console.log(data);
    });
};

// var intval = setInterval(loop, 5000);
loop();