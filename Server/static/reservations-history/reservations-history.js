"use strict"
const reservationsContainer = document.getElementById('reservations');
const user = {id: 1, fullName: 'Mario Rossi'};

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');
AppNavbar.updateNavbar(user);

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(2);

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
    var url = new URL('http://localhost:5000/reservations_history');
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
        activities.forEach(activity => {
            const card = document.createElement('div');
            card.className = 'p-3 border rounded activity-card';
            const title = document.createElement('p');
            title.className = 'activity-card_title';
            title.innerHTML = `${activity.sport} - <a href="/static/company/company.html?companyId=${activity.company_id}&companyName=${activity.company_name}&fromPage=2">${activity.company_name}</a>`;
            card.appendChild(title);
            card.appendChild(createParagraph(`Data: ${activity.date} alle ${activity.time}`));
            card.appendChild(createParagraph(`Numero partecipanti: ${activity.partecipants}`));
            card.appendChild(createParagraph(`Località: ${activity.location}`));
            if (activity.feedback_id) {
                card.appendChild(createParagraph(`Voto feedback: ${activity.score}`));
                if (activity.message) {
                    card.appendChild(createParagraph(`Messaggio feedback: ${activity.message}`));
                }
            } else {
                card.appendChild(createParagraph(`Feedback: nessuno. [LASCIA FEEDBACK]`));
            }
            reservationsContainer.appendChild(card);
        });
    }
}

function createParagraph(textContent) {
    const paragraph = document.createElement('p');
    paragraph.innerText = textContent;
    return paragraph;
}

function handleLogin() {
    window.location.href = "../login/login.html";
}

function logout() {
    localStorage.removeItem('userId');
    localStorage.removeItem('userFullName');
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar({id: null, fullName: ''});
}