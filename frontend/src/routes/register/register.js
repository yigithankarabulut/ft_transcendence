document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;

    // Backend'e istek gönderme (örnek)
    fetch('http://localhost:8004/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone
        })
    })
        .then(response => {
            if (response.ok) {
                alert('Registration successful');
                window.location.href = '../login/login.html';
            } else {
                alert('Registration failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
