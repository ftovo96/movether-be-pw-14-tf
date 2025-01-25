"use strict"
const activitiesContainer = document.getElementById('activities');
const feedbacksContainer = document.getElementById('feedbacks');
const user = LoginManager.getUser();
const company = {id: null, name: null};

let modalRef = null;
let modalReservationId = null;
let modalActivityId = null;


AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');
// AppNavbar.updateNavbar(user);

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(0);

BottomNavigationBar.initBottomNavigationBar('bottom-navigation-bar', 0);

initValues();
loadData();

function initValues() {
    const urlParams = new URLSearchParams(window.location.search);
    company.id = urlParams.get('companyId');
    company.name = urlParams.get('companyName');
    document.getElementById('company-name').innerText = company.name;
    const fromPage = urlParams.get('fromPage');
    if (fromPage) {
        AppSidenav.setActiveMenu(+fromPage);
        BottomNavigationBar.setActiveMenu(+fromPage);
    } else {
        AppSidenav.setActiveMenu(0);
        BottomNavigationBar.setActiveMenu(0);
    }
}

async function loadActivities() {
    activitiesContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.classList = 'query-message';
    loadingElem.innerText = 'Caricamento...';
    activitiesContainer.appendChild(loadingElem);
    const params = {
        'companyId': company.id,
    };
    var url = new URL('http://localhost:5000/activities');
    if (user.id) {
        url.searchParams.append('userId', user.id);
    }
    Object.keys(params)
        .forEach(key => {
            if (!params[key]) return;
            url.searchParams.append(key, params[key])
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
                <div class="flexible-card_badge">${badge}</div>
                <p class="flexible-card_title">
                    ${activity.sport} - <a href="/static/company/company.html?companyId=${activity.company_id}&companyName=${activity.company_name}&fromPage=0">${activity.company_name}</a>
                </p>
                <p><i class="bi bi-calendar-week"></i> Data: ${activity.date}</p>
                <p><i class="bi bi-clock"></i> Orari disponibili: ${activity.times.split('; ').join(' - ')}</p>
                <p><i class="bi bi-people"></i> Posti disponibili: ${activity.max_partecipants}</p>
                <p><i class="bi bi-geo"></i> Località: ${activity.location}</p>
            </div>
            `;
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
            card.classList = 'p-3 border rounded flexible-card';
            if (!isAvailable) {
                card.classList.add('flexible-card_disabled');
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
    if (availablePartecipants === 1) {
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

async function loadData() {
    loadActivities();
    loadFeedbacks();
}

async function loadFeedbacks() {
    feedbacksContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.innerText = '';
    loadingElem.classList = 'query-message';
    feedbacksContainer.appendChild(loadingElem);
    var url = new URL(`http://localhost:5000/feedbacks/${company.id}`);
    const feedbacks = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
        feedbacksContainer.replaceChildren();
    if (!feedbacks.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessun feedback';
        feedbacksContainer.appendChild(noActivitiesElem);
    } else {
        feedbacks.forEach(feedback => {
            const date = new Date(feedback.timestamp).toLocaleDateString();
            // const card = document.createElement('div');
            // card.className = 'p-3 border rounded flexible-card';
            // const filledStars = '<i class="bi bi-star-fill"></i>'.repeat(feedback.score);
            // const emptyStars = '<i class="bi bi-star"></i>'.repeat(5 - feedback.score);
            // card.appendChild(createParagraph(`Voto: ${filledStars}${emptyStars}`));
            // if (feedback.message) {
            //     const title = document.createElement('p');
            //     title.className = 'flexible-card_title';
            //     title.innerHTML = `${feedback.message}`;
            //     card.appendChild(title);
            // }
            // card.appendChild(createParagraph(`${feedback.userName} - ${date}`));
            // feedbacksContainer.appendChild(card);
            const filledStars = '<i class="bi bi-star-fill text-success"></i>'.repeat(feedback.score);
            const emptyStars = '<i class="bi bi-star text-secondary"></i>'.repeat(5 - feedback.score);
            let cardContent = `
                <div>
                    <div>${filledStars}${emptyStars}</div>
                    <p class="flexible-card_title">${feedback.message}</p>
                    <p><i class="bi bi-person-circle"></i> ${feedback.userName} - ${date}</p>
                </div>
            `;
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded flexible-card';
            card.innerHTML = cardContent;
            feedbacksContainer.appendChild(card);
        });
    }
}

function createParagraph(textContent) {
    const paragraph = document.createElement('p');
    paragraph.innerText = textContent;
    return paragraph;
}

function goBack() {
    window.history.back();
}

function logout() {
    LoginManager.logout();
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar(user);
}