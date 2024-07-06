export async function fetchAi() {
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startButton = document.getElementById('startButton');
const scoreBoard = document.getElementById('scoreBoard');

const paddleHeight = 100;
const paddleWidth = 10;
const ballSize = 10;

let playerY = (canvas.height - paddleHeight) / 2;
let aiY = (canvas.height - paddleHeight) / 2;
let ballX = canvas.width / 2;
let ballY = canvas.height / 2;
let ballSpeedX = 5;
let ballSpeedY = 5;

let playerScore = 0;
let aiScore = 0;
let gameRunning = false;

function drawRect(x, y, width, height, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, width, height);
}

function drawCircle(x, y, radius, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2, false);
  ctx.fill();
}

function drawGame() {
  // Clear canvas
  drawRect(0, 0, canvas.width, canvas.height, '#000');
  
  // Draw paddles
  drawRect(0, playerY, paddleWidth, paddleHeight, '#fff');
  drawRect(canvas.width - paddleWidth, aiY, paddleWidth, paddleHeight, '#fff');
  
  // Draw ball
  drawCircle(ballX, ballY, ballSize, '#fff');
}

function moveAI() {
  const aiCenter = aiY + paddleHeight / 2;
  if (aiCenter < ballY - 35) {
    aiY += 6;
  } else if (aiCenter > ballY + 35) {
    aiY -= 6;
  }
}

function updateBall() {
  ballX += ballSpeedX;
  ballY += ballSpeedY;
  
  // Top and bottom collision
  if (ballY < 0 || ballY > canvas.height) {
    ballSpeedY = -ballSpeedY;
  }
  
  // Paddle collision
  if (ballX < paddleWidth) {
    if (ballY > playerY && ballY < playerY + paddleHeight) {
      ballSpeedX = -ballSpeedX;
      const deltaY = ballY - (playerY + paddleHeight / 2);
      ballSpeedY = deltaY * 0.35;
    } else if (ballX < 0) {
      aiScore++;
      resetBall();
    }
  }
  if (ballX > canvas.width - paddleWidth) {
    if (ballY > aiY && ballY < aiY + paddleHeight) {
      ballSpeedX = -ballSpeedX;
      const deltaY = ballY - (aiY + paddleHeight / 2);
      ballSpeedY = deltaY * 0.35;
    } else if (ballX > canvas.width) {
      playerScore++;
      resetBall();
    }
  }
}

function resetBall() {
  ballX = canvas.width / 2;
  ballY = canvas.height / 2;
  ballSpeedX = -ballSpeedX;
  ballSpeedY = Math.random() * 10 - 5;
}

function updateGame() {
  if (!gameRunning) return;
  
  moveAI();
  updateBall();
  drawGame();
  updateScore();
  
  if (playerScore === 5 || aiScore === 5) {
    endGame();
  } else {
    requestAnimationFrame(updateGame);
  }
}

function updateScore() {
  scoreBoard.textContent = `Player: ${playerScore} | AI: ${aiScore}`;
}

function endGame() {
  gameRunning = false;
  const winner = playerScore === 5 ? "Player" : "AI";
  alert(`${winner} wins the game!`);
  startButton.style.display = 'block';
}

function startGame() {
  playerScore = 0;
  aiScore = 0;
  resetBall();
  gameRunning = true;
  startButton.style.display = 'none';
  updateGame();
}

startButton.addEventListener('click', startGame);

document.addEventListener('keydown', (e) => {
  if (e.key === 'w' || e.key === 'ArrowUp') {
    playerY = Math.max(0, playerY - 20);
  } else if (e.key === 's' || e.key === 'ArrowDown') {
    playerY = Math.min(canvas.height - paddleHeight, playerY + 20);
  }
});

drawGame();
}