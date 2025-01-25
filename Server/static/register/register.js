"use strict"

function goBack() {
    window.history.back();
}

function handleSubmit(event) {
    event.preventDefault();
    const name = document.getElementById('user-name').value.trim();
    const surname = document.getElementById('user-surname').value.trim();
    const email = document.getElementById('user-email').value.trim();
    const password = document.getElementById('user-password').value.trim();
    const anyEmptyField = !name || !surname || !email || !password;
    if (anyEmptyField || password.length < 8) {
        const form = document.getElementById('login-form');
        form.classList.remove('needs-validation');
        form.classList.add('was-validated');
        return;
    }
    const userInfo = {
        name, surname, email, password,
    };
    createAccount(userInfo);
}

async function createAccount(userInfo) {
    const response = await LoginManager.register(userInfo);
    if (response.result === 'OK') {
        document.getElementById('user-name').value = '';
        document.getElementById('user-surname').value = '';
        document.getElementById('user-email').value = '';
        document.getElementById('user-password').value = '';
        await LoginManager.login(userInfo.email, userInfo.password);
        window.location.href = "/";
    }
}
