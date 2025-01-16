"use strict"
const activitiesContainer = document.getElementById('activities');
const user = {id: 1, fullName: 'Mario Rossi'};
const company = {id: null, name: null};

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');
AppNavbar.updateNavbar(user);

AppSidenav.initSidenav('sidenav-container');

initValues();
loadActivities();

function initValues() {
    const urlParams = new URLSearchParams(window.location.search);
    company.id = urlParams.get('companyId');
    company.name = urlParams.get('companyName');
    document.getElementById('company-name').innerText = company.name;
    const fromPage = urlParams.get('fromPage');
    if (fromPage) {
        AppSidenav.setActiveMenu(+fromPage);
    } else {
        AppSidenav.setActiveMenu(0);
    }
}

async function loadActivities() {
    activitiesContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.classList = 'query-message';
    loadingElem.innerText = 'Caricamento...';
    activitiesContainer.appendChild(loadingElem);
    await new Promise(r => setTimeout(r, 1000));
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

function createParagraph(textContent) {
    const paragraph = document.createElement('p');
    paragraph.innerText = textContent;
    return paragraph;
}

function goBack() {
    window.history.back();
}

function handleLogin() {
    window.location.href = "../login/login.html";
}

function logout() {
    localStorage.removeItem('userId');
    localStorage.removeItem('userFullName');
    AppNavbar.updateNavbar({id: null, fullName: null});
}