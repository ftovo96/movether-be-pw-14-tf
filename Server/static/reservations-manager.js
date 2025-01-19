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
        reservations[index] = reservation;
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

const ReservationsManager = {
    saveReservation: saveReservation,
    removeReservation: removeReservation,
    getReservations: getReservations,
    clearReservations: clearReservations,
};