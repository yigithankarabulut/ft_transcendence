import { navigateTo } from "../../utils/navTo.js";

export async function fetchLocaltournament() {
    const access_token = localStorage.getItem("access_token");
    if (!access_token) {
        console.log("No access token found");
        navigateTo("/login");
        } else {
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreBoard = document.getElementById('scoreBoard');
            const tournamentInfo = document.getElementById('tournamentInfo');
    
            let players = [];
            let currentMatch = 0;
            let matchWinners = [];
            let finalMatchParticipants = [];
            let gameState = {
                paddle1: { y: 150, score: 0 },
                paddle2: { y: 150, score: 0 },
                ball: { x: 400, y: 200, dx: 5, dy: 5 },
                inProgress: false
            };
            document.getElementById('start-tournement').addEventListener('click', () => {
                players = [
                    document.getElementById('player1').value,
                    document.getElementById('player2').value,
                    document.getElementById('player3').value,
                    document.getElementById('player4').value
                ];
                if (players.some(p => !p)) {
                    alert("Please enter aliases for all players!");
                    return;
                }
                currentMatch = 0;
                matchWinners = [];
                tournamentInfo.innerHTML = `Tournament started!<br>
                                            Match 1: ${players[0]} vs ${players[1]}<br>
                                            Match 2: ${players[2]} vs ${players[3]}`;
                startMatch();
            });
    
            function startMatch() {
                gameState = {
                    paddle1: { y: 150, score: 0 },
                    paddle2: { y: 150, score: 0 },
                    ball: { x: 400, y: 200, dx: 5, dy: 5 },
                    inProgress: true
                };
                scoreBoard.innerHTML = `${players[currentMatch * 2]} 0 - 0 ${players[currentMatch * 2 + 1]}`;
                requestAnimationFrame(gameLoop);
            }
    
            function startFinalMatch(){
                gameState = {
                    paddle1: { y: 150, score: 0 },
                    paddle2: { y: 150, score: 0 },
                    ball: { x: 400, y: 200, dx: 5, dy: 5 },
                    inProgress: true
                };
                requestAnimationFrame(gameLoop);
            }
    
            function gameLoop() {
                update();
                draw();
                if (gameState.inProgress) {
                    requestAnimationFrame(gameLoop);
                }
            }
    
            function update() {
                if (keys.ArrowUp && gameState.paddle2.y > 0) gameState.paddle2.y -= 5;
                if (keys.ArrowDown && gameState.paddle2.y < canvas.height - 100) gameState.paddle2.y += 5;
                if (keys.w && gameState.paddle1.y > 0) gameState.paddle1.y -= 5;
                if (keys.s && gameState.paddle1.y < canvas.height - 100) gameState.paddle1.y += 5;
    
                gameState.ball.x += gameState.ball.dx;
                gameState.ball.y += gameState.ball.dy;
    
                if (gameState.ball.y <= 0 || gameState.ball.y >= canvas.height) {
                    gameState.ball.dy *= -1;
                }
    
                if (
                    (gameState.ball.x <= 20 && gameState.ball.y >= gameState.paddle1.y && gameState.ball.y <= gameState.paddle1.y + 100) ||
                    (gameState.ball.x >= canvas.width - 20 && gameState.ball.y >= gameState.paddle2.y && gameState.ball.y <= gameState.paddle2.y + 100)
                ) {
                    gameState.ball.dx *= -1;
                }
    
                if (gameState.ball.x <= 0) {
                    gameState.paddle2.score++;
                    resetBall();
                } else if (gameState.ball.x >= canvas.width) {
                    gameState.paddle1.score++;
                    resetBall();
                }
    
                if (currentMatch != 2)
                    scoreBoard.innerHTML = `${players[currentMatch * 2]} ${gameState.paddle1.score} - ${gameState.paddle2.score} ${players[currentMatch * 2 + 1]}`;
                else
                    scoreBoard.innerHTML = `${finalMatchParticipants[0]} ${gameState.paddle1.score} - ${gameState.paddle2.score} ${finalMatchParticipants[1]}`;
    
                if (gameState.paddle1.score === 5 || gameState.paddle2.score === 5) {
                    endMatch();
                }
            }
    
            function draw() {
                // Clear canvas
                ctx.fillStyle = '#000';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
    
                // Draw paddles
                ctx.fillStyle = '#fff';
                ctx.fillRect(0, gameState.paddle1.y, 20, 100);
                ctx.fillRect(canvas.width - 20, gameState.paddle2.y, 20, 100);
    
                // Draw ball
                ctx.beginPath();
                ctx.arc(gameState.ball.x, gameState.ball.y, 10, 0, Math.PI * 2);
                ctx.fill();
    
                // Draw center line
                ctx.setLineDash([5, 15]);
                ctx.moveTo(canvas.width / 2, 0);
                ctx.lineTo(canvas.width / 2, canvas.height);
                ctx.stroke();
            }
    
            function resetBall() {
                gameState.ball.x = canvas.width / 2;
                gameState.ball.y = canvas.height / 2;
                gameState.ball.dx = (Math.random() > 0.5 ? 1 : -1) * 5;
                gameState.ball.dy = (Math.random() > 0.5 ? 1 : -1) * 5;
            }
    
            function endMatch() {
                gameState.inProgress = false;
                var winner;
                if (currentMatch != 2)
                {
                    winner = gameState.paddle1.score > gameState.paddle2.score ? players[currentMatch * 2] : players[currentMatch * 2 + 1];
                    matchWinners.push(winner);
                }
                else
                {
                    winner = gameState.paddle1.score > gameState.paddle2.score ? finalMatchParticipants[0] : finalMatchParticipants[1];
                    matchWinners.push(winner);
                }
                currentMatch++;
                console.log("current match is", currentMatch);
                if (currentMatch === 1) {
                    tournamentInfo.innerHTML += `<br>${winner} wins!<br>Next match: ${players[2]} vs ${players[3]}`;
                    setTimeout(startMatch, 3000);
                } else if (currentMatch === 2) {
                    finalMatchParticipants = [...matchWinners];
                    tournamentInfo.innerHTML += `<br>${winner} wins!<br>Final match: ${finalMatchParticipants[0]} vs ${finalMatchParticipants[1]}`;
                    setTimeout(startFinalMatch, 3000);
                } else if (currentMatch === 3) { // Check if final match is completed
                    tournamentInfo.innerHTML += `<br>${matchWinners[2]} wins the tournament!`;
                }
            }
            // Keyboard input
            let keys = {};
            document.addEventListener('keydown', (e) => { keys[e.key] = true; });
            document.addEventListener('keyup', (e) => { keys[e.key] = false; });
        }
    }