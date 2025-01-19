"use strict"
const activitiesContainer = document.getElementById('activities');
const feedbacksContainer = document.getElementById('feedbacks');
const user = LoginManager.getUser();
const company = {id: null, name: null};

let modalRef = null;
let modalReservationId = null;


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
            const card = document.createElement('div');
            card.className = 'p-3 border rounded activity-card';
            const title = document.createElement('p');
            title.className = 'activity-card_title';
            title.innerHTML = `${activity.sport}`;
            card.appendChild(title);
            card.appendChild(createParagraph(`Data: ${activity.date}`));
            card.appendChild(createParagraph(`Orari disponibili: ${activity.times.split('; ').join(' - ')}`));
            card.appendChild(createParagraph(`Posti disponibili: ${activity.max_partecipants}`));
            card.appendChild(createParagraph(`Località: ${activity.location}`));
            activitiesContainer.appendChild(card);
        });
    }
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
            const card = document.createElement('div');
            card.className = 'p-3 border rounded activity-card';
            card.appendChild(createParagraph(`Voto: ${'*'.repeat(feedback.score)}`));
            if (feedback.message) {
                const title = document.createElement('p');
                title.className = 'activity-card_title';
                title.innerHTML = `${feedback.message}`;
                card.appendChild(title);
            }
            card.appendChild(createParagraph(`${feedback.userName}`));
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
    loadReservations();
    updateInterface();
}