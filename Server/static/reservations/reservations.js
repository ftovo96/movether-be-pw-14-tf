"use strict"
const user = LoginManager.getUser();
let modalRef = null;
let modalReservationId = null;

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');
// AppNavbar.updateNavbar(user);

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(1);

BottomNavigationBar.initBottomNavigationBar('bottom-navigation-bar', 1);

const values = {
    search: null,
    sport: null,
    location: null,
};
let timeoutRef = null;

const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', handleSearch);

const sportSelect = document.getElementById('sport-select');
sportSelect.addEventListener('input', handleChangeSport);

const locationSelect = document.getElementById('location-select');
locationSelect.addEventListener('input', handleChangeLocation);

const reservationsContainer = document.getElementById('reservations');

initValues();
updateInterface();
loadReservations();
loadSports();
loadLocations();

function handleSearch(event) {
    values.search = searchInput.value || null;
    loadReservations();
}

function handleChangeSport(event) {
    if (!sportSelect.value || sportSelect.value === 'ALL') {
        values.sport = null;
    } else {
        values.sport = sportSelect.value;
    }
    loadReservations();
}

function handleChangeLocation(event) {
    if (!locationSelect.value || locationSelect.value === 'ALL') {
        values.location = null;
    } else {
        values.location = locationSelect.value;
    }
    loadReservations();
}

function initValues() {
    values.search = searchInput.value || null;
    if (!sportSelect.value || sportSelect.value === 'ALL') {
        values.sport = null;
    } else {
        values.sport = sportSelect.value;
    }
    if (!locationSelect.value || locationSelect.value === 'ALL') {
        values.location = null;
    } else {
        values.location = locationSelect.value;
    }
}

async function loadLocations() {
    var url = new URL('http://localhost:5000/locations');
    const locations = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
    console.log(locations);
    const locationsSelect = document.getElementById('location-select');
    locationsSelect.replaceChildren();
    const allOption = document.createElement('option');
    allOption.value = 'ALL';
    allOption.innerText = 'Tutti';
    locationsSelect.appendChild(allOption);
    locations.forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.innerText = location;
        locationsSelect.appendChild(option);
    });
}

function loadReservations() {
    if (timeoutRef !== null) {
        clearTimeout(timeoutRef);
        console.log('Cancelling timeout...');
    }
    timeoutRef = setTimeout(fetchReservations, 500);
}

async function loadSports() {
    var url = new URL('http://localhost:5000/sports');
    const sports = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
    console.log(sports);
    const sportsSelect = document.getElementById('sport-select');
    sportSelect.replaceChildren();
    const allOption = document.createElement('option');
    allOption.value = 'ALL';
    allOption.innerText = 'Tutti';
    sportsSelect.appendChild(allOption);
    sports.forEach(sport => {
        const option = document.createElement('option');
        option.value = sport;
        option.innerText = sport;
        sportsSelect.appendChild(option);
    });
}

async function fetchReservations() {
    timeoutRef = null;
    console.log('Fetching activities...');
    reservationsContainer.replaceChildren();
    let activities = [];
    if (user.id) {
        const loadingElem = document.createElement('p');
        loadingElem.classList = 'query-message';
        loadingElem.innerText = 'Caricamento...';
        reservationsContainer.appendChild(loadingElem);
        await new Promise(r => setTimeout(r, 1000));
        var url = new URL('http://localhost:5000/reservations');
        url.searchParams.append('userId', user.id)
        Object.keys(values)
            .forEach(key => {
                if (!values[key]) return;
                url.searchParams.append(key, values[key])
            });
        activities = await fetch(url)
            .then(result => result.json())
            .catch(() => []);
        reservationsContainer.replaceChildren();
    } else {
        activities = ReservationsManager.getReservations();
    }
    if (!activities.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessuna attività trovata';
        reservationsContainer.appendChild(noActivitiesElem);
    } else {
        activities.forEach(reservation => {
            let badge;
            const reservationDate = new Date(`${reservation.date} ${reservation.time}`);
            const hasExpired = Date.now() > reservationDate;
            const isExpiring = (Date.now() - reservationDate) < (24 * 60 * 60 * 1000);
            const isDisabled = hasExpired && !isExpiring && reservation.validated === "false";
            if (reservation.validated === "true") {
                badge = `<span class="badge text-bg-success">Validata</span>`;
            } else if (hasExpired && reservation.validated === "false") {
                badge = `<span class="badge text-bg-danger">Scaduta</span>`;
            } else if (hasExpired && !reservation.validated) {
                badge = `<span class="badge text-bg-warning">In attesa di validazione</span>`;
            } else if (isExpiring) {
                badge = `<span class="badge text-bg-warning">In scandenza</span>`;
            } else {
                badge = `<span class="badge text-bg-success">Disponibile</span>`;
            }
            let cardContent = `
                <div>
                    <div class="activity-card_badge">${badge}</div>
                    <p class="activity-card_title">
                        ${reservation.sport} - <a href="/static/company/company.html?companyId=${reservation.company_id}&companyName=${reservation.company_name}&fromPage=1">${reservation.company_name}</a>
                    </p>
                    <p><i class="bi bi-calendar-week"></i> Data: ${new Date(reservation.date).toLocaleDateString()} alle ${reservation.time}</p>
                    <p><i class="bi bi-clock"></i> Posti disponibili: ${reservation.max_partecipants}</p>
                    <p><i class="bi bi-people"></i> Posti riservati: ${reservation.partecipants}</p>
                    <p><i class="bi bi-geo"></i> Località: ${reservation.location}</p>
                </div>
            `;
            if (Date.now() < new Date(`${reservation.date} ${reservation.time}`)) {
                cardContent += `<div class="activity-cart_actions">
                    <button class="btn btn-primary" onclick="showEditReservationModal('${reservation.id}')">Modifica</button>
                    <button class="btn btn-danger" onclick="showDeleteReservationModal('${reservation.id}')">Elimina</button>
                </div>`
            } else if (reservation.validated === "true" && !reservation.feedbackId) {
                cardContent += `<div class="activity-cart_actions">
                    <button class="btn btn-primary" onclick="showFeedbackModal('${reservation.id}')">Lascia Feedback</button>
                </div>`
            }
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded activity-card';
            if (isDisabled) {
                card.classList.add('activity-card_disabled');
            }
            card.innerHTML = cardContent;
            reservationsContainer.appendChild(card);
        });
    }
}

function showDeleteReservationModal(reservationId) {
    const modal = document.getElementById('reservationDeleteModal');
    modalRef = new bootstrap.Modal(modal);
    modalRef.show();
    modalReservationId = reservationId;
}

async function deleteReservation() {
    var url = new URL(`http://localhost:5000/deleteReservation/${modalReservationId}`);
    await fetch(url, { method: 'DELETE', })
        .then(result => {
            if (result.status === 200) {
                modalRef.hide();
                modalRef = null;
                modalReservationId = null;
                loadReservations();
            }
        });
}

async function showEditReservationModal(reservationId) {
    var url = new URL(`http://localhost:5000/reservations/${reservationId}`);
    // if (user.id) {
    //     url.searchParams.append('userId', user.id);
    // }
    const activities = await fetch(url)
        .then(result => result.json());
    console.log('Edit Reservation ' + reservationId);
    const modal = document.getElementById('reservationEditModal');
    document.getElementById('reservationEditModalTitle').innerText = `Modifica prenotazione ${reservationId}`;
    // Imposto orari selezionabili
    const timeSelect = document.getElementById('time-select');
    timeSelect.disabled = false;
    timeSelect.replaceChildren();
    activities.forEach((activity, index) => {
        const option = document.createElement('option');
        option.value = activity.time;
        option.innerText = activity.time;
        if (index === 0) {
            option.selected = true;
        }
        timeSelect.appendChild(option);

    });
    if (activities.length === 1) {
        timeSelect.disabled = true;
    }
    // Imposto posti selezionabili
    const partecipantsSelect = document.getElementById('partecipants-select');
    partecipantsSelect.disabled = false;
    partecipantsSelect.replaceChildren();
    const availablePartecipants = activities[0].availablePartecipants;
    for (var i = 1; i <= availablePartecipants; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.innerText = i;
        if (i === 1) {
            option.selected = true;
        }
        partecipantsSelect.appendChild(option);
    }
    if (availablePartecipants === 1 || !LoginManager.isLoggedIn()) {
        partecipantsSelect.disabled = true;
    }
    modalRef = new bootstrap.Modal(modal);
    modalRef.show();
    modalReservationId = reservationId;
}

async function editReservation() {
    var url = new URL(`http://localhost:5000/reservations/${modalReservationId}`);
    // if (user.id) {
    //     url.searchParams.append('userId', user.id);
    // }
    const activities = await fetch(url)
        .then(result => result.json());
    const time = document.getElementById('time-select').value;
    const partecipants = document.getElementById('partecipants-select').value;
    const activity = activities.find(activity => activity.time === time);
    console.log(`Reserve activity ${activity.id} at time ${time} for ${partecipants} people`);
    await fetch(`http://localhost:5000/updateReservation/${modalReservationId}`, {
        method: 'PUT',
        body: JSON.stringify({
            "activityId": activity.id,
            // "time": time,
            "partecipants": partecipants,
            "userId": user.id,
        }),
    })
        .then(result => {
            if (result.status === 200) {
                modalRef.hide();
                modalRef = null;
                modalReservationId = null;
                loadReservations();
            }
        });
}

function showFeedbackModal(reservationId) {
    document.getElementById('feedback-score').value = '';
    document.getElementById('feedback-message').value = '';
    const modal = document.getElementById('feedbackModal');
    modalRef = new bootstrap.Modal(modal);
    modalRef.show();
    modalReservationId = reservationId;
}

async function saveFeedback() {
    const feedbackScore = document.getElementById('feedback-score').value;
    const feedbackMessage = document.getElementById('feedback-message').value.trim();
    if (!feedbackScore) {
        const form = document.getElementById('feedback-form');
        form.classList.remove('needs-validation');
        form.classList.add('was-validated');
        return;
    }
    await fetch(`http://localhost:5000/send-feedback/${modalReservationId}`, {
            method: 'POST',
            body: JSON.stringify({
                "score": feedbackScore,
                "message": feedbackMessage || null,
                "userId": user.id,
            }),
        })
        .then(result => {
            if (result.status === 200) {
                modalRef.hide();
                modalRef = null;
                modalReservationId = null;
                loadReservations();
            }
        });
}

function showManageAnonymousReservationModal() {
    document.getElementById('reservation-number').value = '';
    document.getElementById('reservation-security-code').value = '';
    document.getElementById('anonymous-reservation-error-container').classList.add('d-none');
    const modal = document.getElementById('anonymousReservationModal');
    modalRef = new bootstrap.Modal(modal);
    modalRef.show();
}

async function addReservation() {
    const errorContainer = document.getElementById('anonymous-reservation-error-container');
    errorContainer.classList.add('d-none');
    const reservationNumber = document.getElementById('reservation-number').value.trim();
    const reservationSecurityCode = document.getElementById('reservation-security-code').value.trim();
    if (!reservationNumber || !reservationSecurityCode) {
        const form = document.getElementById('anonymous-reservation-form');
        form.classList.remove('needs-validation');
        form.classList.add('was-validated');
        return;
    }
    // Get reservation
    await new Promise(r => setTimeout(r, 1000));
    var url = new URL('http://localhost:5000/get-reservation-by-code');
    url.searchParams.append('id', reservationNumber);
    url.searchParams.append('securityCode', reservationSecurityCode);
    const reservation = await fetch(url)
        .then(result => result.json())
        .catch(() => null);
    if (reservation) {
        // Se reservation esiste
        if (!user.id) {
            // Se utente non loggato aggiungi a localstorage
            ReservationsManager.addReservation(reservation);
        } else {
            // Se utente loggato associa ad utente corrente
            // Se ok ricarica lista prenotazioni
            loadReservations();
            // Se errore (perchè già associata) mostra errore
        }
    } else {
        errorContainer.classList.remove('d-none');
        errorContainer.innerText = 'Prenotazione non trovata. Verificare che il numero di prenotazione e il codice segreto siano corretti.';
        // Se non esiste mostra errore
    }
}

function logout() {
    LoginManager.logout();
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar(user);
    loadReservations();
    updateInterface();
}

function updateInterface() {
    if (user.id) {
        document.getElementById('filters').classList.remove('d-none');
        document.getElementById('logged-in-info').classList.remove('d-none');
        document.getElementById('anonymous-info').classList.add('d-none');
    } else {
        searchInput.value = '';
        sportSelect.value = 'ALL';
        locationSelect.value = 'ALL';
        values.search = null;
        values.location = null;
        values.sport = null;
        document.getElementById('filters').classList.add('d-none');
        document.getElementById('anonymous-info').classList.remove('d-none');
        document.getElementById('logged-in-info').classList.add('d-none');
    }
    searchInput.disabled = !user.id;
    sportSelect.disabled = !user.id;
    locationSelect.disabled = !user.id;
}

window.addEventListener('pageshow', () => {
    const currentUser = LoginManager.getUser();
    if (currentUser.id !== user.id) {
        user.id = currentUser.id;
        user.fullName = currentUser.fullName;
        updateInterface();
        loadReservations();
    } else {
        updateInterface();
    }
});