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
    console.log(values);
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
    const activities = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
        reservationsContainer.replaceChildren();
    if (!activities.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessuna attività trovata';
        reservationsContainer.appendChild(noActivitiesElem);
    } else {
        activities.forEach(reservation => {
            const cardContent = `
                <div>
                    <p class="activity-card_title">
                        ${reservation.sport} - <a href="/static/company/company.html?companyId=${reservation.company_id}&companyName=${reservation.company_name}&fromPage=0">${reservation.company_name}</a>
                    </p>
                    <p>Data: ${reservation.date} alle ${reservation.time}</p>
                    <p>Posti disponibili: ${reservation.max_partecipants}</p>
                    <p>Posti riservati: ${reservation.partecipants}</p>
                    <p>Località: ${reservation.location}</p>
                </div>
                <div class="activity-cart_actions">
                    <button class="btn btn-primary" onclick="showEditReservationModal('${reservation.id}')">Modifica</button>
                    <button class="btn btn-danger" onclick="showDeleteReservationModal('${reservation.id}')">Elimina</button>
                </div>
            `;
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded activity-card';
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
    if (availablePartecipants === 1) {
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

function logout() {
    LoginManager.logout();
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar(user);
    loadReservations();
}

window.addEventListener('pageshow', () => {
    console.log('x');
    const currentUser = LoginManager.getUser();
    if (currentUser.id !== user.id) {
        user.id = currentUser.id;
        user.fullName = currentUser.fullName;
        loadReservations();
    }
});