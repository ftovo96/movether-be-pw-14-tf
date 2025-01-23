"use strict"
const user = LoginManager.getUser();
let modalRef = null;
let modalActivityId = null;

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(0);

BottomNavigationBar.initBottomNavigationBar('bottom-navigation-bar', 0);

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

const activitiesContainer = document.getElementById('activities');

// updateUser();
initValues();
loadActivities();
loadSports();
loadLocations();

// function getCookie(cookieName) {
//     return document.cookie
//         .split("; ")
//         .find((cookie) => cookie.startsWith(cookieName + "="))
//         ?.split("=")[1] || null;
// }

function handleSearch(event) {
    values.search = searchInput.value || null;
    loadActivities();
}

function handleChangeSport(event) {
    if (!sportSelect.value || sportSelect.value === 'ALL') {
        values.sport = null;
    } else {
        values.sport = sportSelect.value;
    }
    loadActivities();
}

function handleChangeLocation(event) {
    if (!locationSelect.value || locationSelect.value === 'ALL') {
        values.location = null;
    } else {
        values.location = locationSelect.value;
    }
    loadActivities();
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

function loadActivities() {
    if (timeoutRef !== null) {
        clearTimeout(timeoutRef);
        console.log('Cancelling timeout...');
    }
    timeoutRef = setTimeout(fetchActivities, 250);
}

async function loadLocations() {
    var url = new URL('http://localhost:5000/locations');
    const locations = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
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

async function loadSports() {
    var url = new URL('http://localhost:5000/sports');
    const sports = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
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

async function fetchActivities() {
    timeoutRef = null;
    console.log('Fetching activities...');
    activitiesContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.classList = 'query-message';
    loadingElem.innerText = 'Caricamento...';
    activitiesContainer.appendChild(loadingElem);
    await new Promise(r => setTimeout(r, 1000));
    var url = new URL('http://localhost:5000/activities');
    if (user.id) {
        url.searchParams.append('userId', user.id);
    }
    Object.keys(values)
        .forEach(key => {
            if (!values[key]) return;
            url.searchParams.append(key, values[key]);
        });
    const activities = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
    activitiesContainer.replaceChildren();
    if (!activities.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessuna attività trovata';
        activitiesContainer.appendChild(noActivitiesElem);
    } else {
        activities.forEach(activity => {
            // const card = document.createElement('div');
            // card.className = 'p-3 border rounded activity-card';
            // const title = document.createElement('p');
            // title.className = 'activity-card_title';
            // title.innerHTML = `${activity.sport} - <a href="/static/company/company.html?companyId=${activity.company_id}&companyName=${activity.company_name}&fromPage=0">${activity.company_name}</a>`;
            // card.appendChild(title);
            // card.appendChild(createParagraph(`Data: ${activity.date}`));
            // card.appendChild(createParagraph(`Orari disponibili: ${activity.times.split('; ').join(' - ')}`));
            // card.appendChild(createParagraph(`Posti disponibili: ${activity.max_partecipants}`));
            // card.appendChild(createParagraph(`Località: ${activity.location}`));
            // const buttonContainer = document.createElement('div');
            // const button = document.createElement('button');
            // button.className = 'btn btn-primary';
            // button.onclick = `reserveActivity(${activity.id})`;
            // button.innerText = 'Prenota';
            // buttonContainer.appendChild
            let badge;
            let isAvailable;
            if (LoginManager.isLoggedIn()) {
                badge = `<span class="badge text-bg-success">Disponibile</span>`;
                isAvailable = true;
            } else if (activity.allowAnonymous === "true") {
                badge = `<span class="badge text-bg-primary">Prenotazione anonima</span>`;
                isAvailable = true;
            } else {
                badge = `<span class="badge text-bg-danger">Non disponibile</span>`;
                isAvailable = false;
            }
            if (activity.isBanned) {
                isAvailable = false;
            }
            let cardContent = `
                <div>
                    <div class="activity-card_badge">${badge}</div>
                    <p class="activity-card_title">
                        ${activity.sport} - <a href="/static/company/company.html?companyId=${activity.company_id}&companyName=${activity.company_name}&fromPage=0">${activity.company_name}</a>
                    </p>
                    <p><i class="bi bi-calendar-week"></i> Data: ${new Date(activity.date).toLocaleDateString()}</p>
                    <p><i class="bi bi-clock"></i> Orari disponibili: ${activity.times.split('; ').join(' - ')}</p>
                    <p><i class="bi bi-people"></i> Posti disponibili: ${activity.max_partecipants}</p>
                    <p><i class="bi bi-geo"></i> Località: ${activity.location}</p>
                </div>`;
            if (isAvailable) {
                cardContent += `<div class="activity-cart_actions">
                        <button class="btn btn-primary" onclick="showReserveActivityModal('${activity.id}')">Prenota</button>
                    </div>`;
            } else if (activity.isBanned) {
                cardContent += `
                    <div class="alert alert-danger" role="alert">
                        Hai effettuato troppe prenotazioni non godute!
                    </div>
                `;
            }
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded activity-card';
            if (!isAvailable) {
                card.classList.add('activity-card_disabled');
            }
            card.innerHTML = cardContent;
            activitiesContainer.appendChild(card);
        });
    }
}

async function showReserveActivityModal(activityId) {
    var url = new URL(`http://localhost:5000/activities/${activityId}`);
    if (user.id) {
        url.searchParams.append('userId', user.id);
    }
    const activities = await fetch(url)
        .then(result => result.json());
    console.log('ReserveActivity ' + activityId);
    const modal = document.getElementById('reservationModal');
    document.getElementById('reservationModalTitle').innerText = `Prenota attività ${activityId}`;
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
    modalActivityId = activityId;
}

async function reserveActivity() {
    var url = new URL(`http://localhost:5000/activities/${modalActivityId}`);
    if (user.id) {
        url.searchParams.append('userId', user.id);
    }
    const activities = await fetch(url)
        .then(result => result.json());
    const time = document.getElementById('time-select').value;
    const partecipants = document.getElementById('partecipants-select').value;
    const activity = activities.find(activity => activity.time === time);
    console.log(`Reserve activity ${activity.id} at time ${time} for ${partecipants} people`);
    const reservation = await fetch('http://localhost:5000/reserveActivity', {
            method: 'POST',
            body: JSON.stringify({
                "activityId": activity.id,
                "time": time,
                "partecipants": partecipants,
                "userId": user.id,
                "reservationId": activity.reservationId,
            }),
        })
        .then(result => result.json())
        .catch(err => null);
    if (reservation) {
        if (!LoginManager.isLoggedIn()) {
            ReservationsManager.saveReservation(reservation);
            showReservationCodeModal(reservation);
        }
        modalRef.hide();
        modalRef = null;
        modalActivityId = null;
        loadActivities();
    }
}

function showReservationCodeModal(reservation) {
    document.getElementById('reservation-number').innerText = reservation.id;
    document.getElementById('reservation-security-code').innerText = reservation.securityCode;
    const modal = document.getElementById('reservationCodeModal');
    new bootstrap.Modal(modal).show();
}

// function createParagraph(textContent) {
//     const paragraph = document.createElement('p');
//     paragraph.innerText = textContent;
//     return paragraph;
// }

// async function login() {
//     const response = await fetch('http://localhost:5000/login')
//         .then(result => result.json());
//     if (response.result === 'OK') {
//         localStorage.setItem('userId', response.user.id);
//         localStorage.setItem('userFullName', response.user.name + ' ' + response.user.surname);
//         user.id = localStorage.getItem('userFullName');
//         user.fullName = localStorage.getItem('userFullName');
//         updateUserDropdown();
//     } else {
//         logout();
//     }
// }

// function handleLogin() {
//     window.location.href = "login.html";
// }

function logout() {
    LoginManager.logout();
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar(user);
    loadActivities();
}

// window.addEventListener('popstate', function(event) {
//     // Your JavaScript code to run when the user navigates back
//     console.log('Navigated back to this page');
//     // Add your specific logic here
// });

// window.onload = (event) => {
//     console.log("page is fully loaded");
// };

// window.onpageshow = function() {
//     updateUser();
// };

window.addEventListener('pageshow', () => {
    const currentUser = LoginManager.getUser();
    if (currentUser.id !== user.id) {
        user.id = currentUser.id;
        user.fullName = currentUser.fullName;
        // updateInterface();
        loadActivities();
    } else {
        // updateInterface();
    }
});