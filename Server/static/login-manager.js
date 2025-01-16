"use strict"
const LoginManager = {
    isLoggedIn: () => {
        return localStorage.getItem('userId') !== null;
    },
    getUser: () => {
        const user = {
            id: localStorage.getItem('userId'),
            fullName: localStorage.getItem('userFullName'),
        };
        return user;
    },
    login: async (email, password) => {
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            body: JSON.stringify({
                "email": email,
                "password": password,
            }),
        })
        .then(result => result.json());
        if (response.result === 'OK') {
            localStorage.setItem('userId', response.user.id);
            const userFullName = response.user.name + ' ' + response.user.surname;
            localStorage.setItem('userFullName', userFullName);
        }
        return response;
    },
    logout: () => {
        localStorage.removeItem('userId');
        localStorage.removeItem('userFullName');
    },
};