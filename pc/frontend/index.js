document.onkeydown = updateKey;
document.onkeyup = resetKey;
window.onload = periodicallyGetCarData;
    
var server_addr = "192.168.1.184";
var server_port = 8080;

function sendRequest(request, responseCallback) {
    const net = require('net');
    
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
        client.write(request);
    });
    
    client.on('data', (response) => {
        responseCallback(response);
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function sendCommand(command) {
    sendRequest(`POST ${command}`, (response) => {
        console.log(response);
    });
}

function updateCarOnMap(location) {
    console.log(location)

    let pointSize = 4;
    let canvas = document.getElementById("map");
    let ctx = canvas.getContext("2d");
    let canvasX = location[0] + canvas.width/2;
    let canvasY = canvas.height/2 - location[1];
    
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
  	ctx.fillStyle = "#ff2626";
    ctx.beginPath();
    ctx.arc(canvasX, canvasY, pointSize, 0, Math.PI * 2, true);
    ctx.fill();
}

function getCarData() {
    sendRequest("GET", (response) => {
        console.log(response);
        let carData = JSON.parse(response);
        let location = [parseInt(carData["location"][0], 10), parseInt(carData["location"][1], 10)];
        let direction = carData["direction"];
        
        document.getElementById("direction").innerHTML = `[${direction[0]}, ${direction[1]}]`;
        document.getElementById("location").innerHTML = `[${location[0]}, ${location[1]}]`;
        document.getElementById("speed").innerHTML = carData["speed"];
        document.getElementById("distance").innerHTML = parseInt(carData["total_distance"], 10);
        document.getElementById("temperature").innerHTML = carData["temperature"];
        document.getElementById("battery").innerHTML = carData["battery"];
        updateCarOnMap(location);
    });
}

function updateKey(e) {
    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        sendCommand("accelerate");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        sendCommand("brake");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        sendCommand("left");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        sendCommand("right");
    }
}

// reset the key to the start state 
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

function periodicallyGetCarData() {
    setInterval(function() {
        getCarData();
    }, 1000);
}
