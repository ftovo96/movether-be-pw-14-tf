"use strict"
const LoginManager = {
    isLoggedIn: () => {
        return localStorage.getItem('userId') !== null;
    },
    getUserIdentifier: () => {
        const savedUserIdentifier = localStorage.getItem('userIdentifier');
        if (savedUserIdentifier) {
            return savedUserIdentifier;
        }
        const userIdentifier = 'abc123';
        localStorage.setItem('userIdentifier', userIdentifier);
        return;
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
            // Provo ad associare le prenotazioni nel localStorage all'utente...
            ReservationsManager.clearReservations();
        }
        return response;
    },
    logout: () => {
        localStorage.removeItem('userId');
        localStorage.removeItem('userFullName');
        ReservationsManager.clearReservations();
    },
};