var quickplay_button = document.getElementById('quickplay');
var tournament_button = document.getElementById('tournament');
var message_div = document.createElement('div');

quickplay_button.addEventListener('click', function() {
    quickplay_button.style.display = 'none';
    tournament_button.style.display = 'none';
    message_div.textContent = "Searching...";
    message_div.style.position = 'fixed';
    message_div.style.top = '50%';
    message_div.style.left = '50%';
    message_div.style.transform = 'translate(-50%, -50%)';

    document.body.appendChild(message_div);
});

