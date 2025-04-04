"use strict"
const AppSidenav = {
    initSidenav: (containerId) => {
        const navbar = `
            <div class="bg-primary-subtle d-none d-lg-block app-sidenav">
            <h1 class="ps-3 pe-3">Movether</h1>
            <div class="d-flex flex-column justify-content-center p-3 app-sidenav_content">
                <div id="sidenav-menu" class="d-grid gap-2">
                    <a href="/static/activities/activities.html" class="btn btn-outline-primary" tabindex="-1" role="button">
                        <i class="bi bi-person-arms-up"></i>
                        Attività
                    </a>
                    <a href="/static/reservations/reservations.html" class="btn btn-outline-primary" tabindex="-1" role="button">
                        <i class="bi bi-calendar-week"></i>
                        Prenotazioni
                    </a>
                    <!--<a href="/static/reservations-history/reservations-history.html" class="btn btn-outline-primary" tabindex="-1" role="button">Storico prenotazioni</a>-->
                    <a href="/static/rewards/rewards.html" class="btn btn-outline-primary" tabindex="-1" role="button">
                        <i class="bi bi-gift"></i>
                        Premi
                    </a>
                </div>
            </div>
        </div>`;
        document.getElementById(containerId).innerHTML = navbar;
    },
    setActiveMenu: (index) => {
        const children = document.getElementById('sidenav-menu').children;
        for (let i = 0; i < children.length; i++) {
            if (i === index) {
                children[i].classList.remove('btn-outline-primary');
                children[i].classList.add('btn-primary');
            } else {
                children[i].classList.add('btn-outline-primary');
                children[i].classList.remove('btn-primary');
            }
        }
    }
};