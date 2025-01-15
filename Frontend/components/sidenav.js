"use strict"
const AppSidenav = {
    initSidenav: (containerId) => {
        const navbar = `
            <div class="bg-secondary-subtle d-none d-lg-block app-sidenav">
            <h1>Sidenav</h1>
            <div class="d-flex flex-column justify-content-center p-3 app-sidenav_content">
                <div id="sidenav-menu" class="d-grid gap-2">
                    <button class="btn btn-outline-primary" type="button">Attività</button>
                    <button class="btn btn-outline-primary" type="button">Le mie prenotazioni</button>
                    <button class="btn btn-outline-primary" type="button">Storico prenotazioni</button>
                    <button class="btn btn-outline-primary" type="button">Premi</button>
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