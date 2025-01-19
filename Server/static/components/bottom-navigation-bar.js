"use strict"
const BottomNavigationBar = {
    initBottomNavigationBar: initBottomNavigationBar,
    setActiveMenu: setActiveMenu,
};

function initBottomNavigationBar(containerId, menuIndex) {
    const navbar = `
        <div id="bottom-navigation-bar-menu" class="bottom-navigation-bar bg-primary-subtle">
            <a href="/static/activities/activities.html" class="btn btn-outline-primary" tabindex="-1" role="button">Attività</a>
            <a href="/static/reservations/reservations.html" class="btn btn-outline-primary" tabindex="-1" role="button">Prenotazioni</a>
            <!--<a href="/static/reservations-history/reservations-history.html" class="btn btn-outline-primary" tabindex="-1" role="button">Storico prenotazioni</a>-->
            <a href="/static/awards/awards.html" class="btn btn-outline-primary" tabindex="-1" role="button">Premi</a>
        </div>`;
    document.getElementById(containerId).innerHTML = navbar;
    setActiveMenu(menuIndex);
}

function setActiveMenu(menuIndex) {
    const children = document.getElementById('bottom-navigation-bar-menu').children;
    for (let i = 0; i < children.length; i++) {
        if (i === menuIndex) {
            children[i].classList.remove('btn-outline-primary');
            children[i].classList.add('btn-primary');
        } else {
            children[i].classList.add('btn-outline-primary');
            children[i].classList.remove('btn-primary');
        }
    }
}