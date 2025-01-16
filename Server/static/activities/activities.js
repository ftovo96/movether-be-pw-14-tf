"use strict"
const user = LoginManager.getUser();

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(0);

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
    timeoutRef = setTimeout(fetchActivities, 500);
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
    Object.keys(values)
        .forEach(key => {
            if (!values[key]) return;
            url.searchParams.append(key, values[key])
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
            const card = document.createElement('div');
            card.className = 'p-3 border rounded activity-card';
            const title = document.createElement('p');
            title.className = 'activity-card_title';
            title.innerHTML = `${activity.sport} - <a href="/static/company/company.html?companyId=${activity.company_id}&companyName=${activity.company_name}&fromPage=0">${activity.company_name}</a>`;
            card.appendChild(title);
            card.appendChild(createParagraph(`Data: ${activity.date}`));
            card.appendChild(createParagraph(`Orari disponibili: ${activity.times.split('; ').join(' - ')}`));
            card.appendChild(createParagraph(`Posti disponibili: ${activity.max_partecipants}`));
            card.appendChild(createParagraph(`Località: ${activity.location}`));
            activitiesContainer.appendChild(card);
        });
    }
}

function createParagraph(textContent) {
    const paragraph = document.createElement('p');
    paragraph.innerText = textContent;
    return paragraph;
}

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
    updateUser();
}

function updateUser() {
    const userData = LoginManager.getUser();
    user.id = userData.id;
    user.fullName = userData.fullName;
    AppNavbar.updateNavbar(user);
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