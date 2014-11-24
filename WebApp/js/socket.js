function JavaSocket(port) {
    var connection;

    console.log("Attempting to connect to server");
    connection = new WebSocket("ws://localhost:" + port.toString() + "/");

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log(e.data);
        chart1.series[0].addPoint([e.data, 5*Math.random()], true, true);
    };

    connection.onopen = function (e) {
        console.log("Connection successfully open...");
    }

    connection.onclose = function (e) {
        console.log("Connection successfully closed...");
    }

    this.terminate = function () {
        console.log("Attempting to close connection with server...");
        connection.close()
    }
}