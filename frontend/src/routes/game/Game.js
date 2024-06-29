import { gameData } from "../quickplay/Quickplay";

const canvas = document.getElementById("canvas-pong");
const ctx = canvas.getContext("2d");

function sendMessage() {
    const message = gameData.room_name;
    const connection = "ws://localhost:8010/ws/game/" + "?room=" + message;
    let ws = new WebSocket(connection);

    ws.onopen = () => {
        console.log("Connected to server");
    }

    function drawPaddles(paddLeft, paddRight) {
        ctx.fillStyle = "white";
        ctx.fillRect(paddLeft.positionX, paddLeft.positionY, paddLeft.sizeX, paddLeft.sizeY);

        ctx.fillStyle = "white";
        ctx.fillRect(paddRight.positionX, paddRight.positionY, paddRight.sizeX, paddRight.sizeY);

        ctx.font = '30px Arial';
        ctx.fillText(paddRight.score, 50, 50);
        ctx.fillText(paddLeft.score, canvas.width - 50, 50);
    }

    function drawBall(ball) {
        ctx.beginPath();
        ctx.arc(ball.positionX, ball.positionY, ball.size, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
        ctx.closePath();
    }

    ws.onmessage = (message) => {
        let items = JSON.parse(message.data);
        console.log(items);
        if (items.message === "game_over" && items.winner) {
            ctx.font = '30px Arial';
            ctx.fillText("Game Over", canvas.width / 2 - 100, canvas.height / 2);
            const winner = "Player " + items.winner + " wins!";
            console.log("winner: ", winner);
            ctx.fillText(winner, canvas.width / 2 - 100, canvas.height / 2 + 50);
            return;
        } else if (items.message === "game_run") {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // ctx.fillStyle = "white";
            // ctx.fillRect(canvas.width / 2, 0, 1, canvas.height);
            drawPaddles(items.padd_left, items.padd_right);
            drawBall(items.ball);
        }
    }

    ws.onclose = () => {
        console.log("Disconnected from server");
    }

    ws.onerror = () => {
        console.log("Error connecting to server");
    }

    document.addEventListener("keydown", function(event) {
        if (event.key === "w" || event.key === "s") {
            ws.send(keys[event.keyCode]);
        }
    });
}

const keys = {
    87: "w",
    83: "s",
};

window.sendMessage = sendMessage;
