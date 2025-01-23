"use strict"
const LoginManager = {
    isLoggedIn: () => {
        return localStorage.getItem('userId') !== null;
    },
    getUser: () => {
        const user = {
            id: localStorage.getItem('userId'),
            fullName: localStorage.getItem('abc'),
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
            localStorage.setItem('abc', userFullName);
        }
        return response;
    },
    // logout: () => {
    //     localStorage.setItem('userId', null);
    //     localStorage.setItem('userFullName', null);
    // },
};
// (() => {
//     // localStorage.setItem('userId', 1);
// })();