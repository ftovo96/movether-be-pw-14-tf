"use strict"

/**
 * @param {Reservation} reservation 
 * @description Salva la prenotazione nel localStorage.
 * Se già presente la aggiorna.
 */
function saveReservation(reservation) {
    const reservations = getReservations();

    if (reservation.length) {
        const index = reservations.findIndex(res => res.id === reservation.id);
        if (index !== -1) {
            reservations[index] = reservation;
        } else {
            reservations.push(reservation);
        }
    } else {
        reservations.push(reservation);
    }
    localStorage.setItem('reservations', JSON.stringify(reservations));
}

/**
 * @param {number} reservationId 
 * @returns {void}
 * @description Rimuove la prenotazione indicata dal
 * localStorage.
 */
function removeReservation(reservationId) {
    const reservations = getReservations();
    const index = reservations.findIndex(res => res.id === reservationId);
    reservations.splice(index, 1);
    localStorage.setItem('reservations', JSON.stringify(reservations));
}

/**
 * @description Restituisce la lista delle prenotazioni salvate
 * o una lista vuota.
 * @returns {Array}
 */
function getReservations() {
    const savedReservations = localStorage.getItem('reservations');
    let reservations;
    if (savedReservations) {
        reservations = JSON.parse(savedReservations);
    } else {
        reservations = [];
    }
    return reservations;
}

/**
 * @description Rimuove tutte le prenotazioni salvate
 * dal localStorage
 */
function clearReservations() {
    localStorage.removeItem('reservations');
}

/**
 * 
 * @param {number} userId Id dell'utente a cui associare le prenotazioni
 * "anonime" (cioè create senza aver effettuato l'accesso).
 */
async function linkReservations(userId) {
    const reservations = getReservations();
    if (!reservations.length) {
        return 0;
    }
    const reservationIds = reservations
        .filter(reservation => !reservation.userId)
        .map(reservation => reservation.id);
    if (!reservationIds.length) {
        return 0;
    }
    const response = await fetch('http://localhost:5000/link-reservations', {
        method: 'POST',
        body: JSON.stringify({
            "reservationIds": reservationIds,
            "userId": userId,
        }),
    })
    .then(result => result.json());
    if (response.result === 'OK') {
    }
    return response;
}

const ReservationsManager = {
    saveReservation: saveReservation,
    removeReservation: removeReservation,
    getReservations: getReservations,
    clearReservations: clearReservations,
    linkReservations: linkReservations,
};