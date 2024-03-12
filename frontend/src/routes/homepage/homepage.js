document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Backend'e istek gönderme
    fetch('http://example.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email, password: password })
    })
        .then(response => {
            if (response.ok) {
                window.location.href = 'homepage.html'; // Giriş başarılıysa anasayfaya yönlendir
            } else {
                alert('Login failed'); // Giriş başarısızsa kullanıcıya hata mesajı göster
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
