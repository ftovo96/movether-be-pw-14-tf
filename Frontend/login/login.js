"use strict"
function handleSubmit(event) {
    event.preventDefault();
    const email = document.getElementById('user-email').value;
    const password = document.getElementById('user-password').value;
    if (!email || !password) {
        const form = document.getElementById('login-form');
        form.classList.remove('needs-validation');
        form.classList.add('was-validated');
        return;
    }
    login(email, password);
}

async function login(email, password) {
    const response = await LoginManager.login(email, password);
    if (response.result === 'OK') {
        document.getElementById('user-email').value = '';
        document.getElementById('user-password').value = '';
        document.getElementById('login-error').classList.add('d-none');
        window.history.back();
    } else {
        document.getElementById('login-error').classList.remove('d-none');
    }
}