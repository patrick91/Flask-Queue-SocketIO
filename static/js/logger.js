$(function() {
    var id = 1;
    var $table = $('table tbody');

    var WEB_SOCKET_SWF_LOCATION = '/static/js/socketio/WebSocketMain.swf',
        socket = io.connect('/log');

    socket.on('log', function (type, message) {
        createMessage(type, message)
    });

    socket.on('error', function (e) {
       console.error('Socket Error', arguments);
    });

    function createMessage(type, message) {
        var row = '<tr><td>' + id + '</td><td>' + type + '</td><td>' + message + '</td></tr>'

        id++;

        $table.append(row);
    }
});