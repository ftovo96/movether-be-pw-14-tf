"use strict"
const AppNavbar = {
    initNavbar: initNavbar,
    updateNavbar: updateNavbar,
};

function initNavbar(containerId, onLogin, onLogout) {
    const navbar = `
        <div class="navbar">
            <div id="user-logged-in" class="dropdown d-none">
                <button class="btn dropdown-toggle navbar-dropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <div id="user-avatar" class="rounded-circle user-avatar"></div>
                    <span id="user-full-name">Nome utente</span>
                </button>
                <ul class="dropdown-menu">
                  <!--<li><a class="dropdown-item">Profilo</a></li>
                  <li><hr class="dropdown-divider"></li>-->
                  <li><button class="dropdown-item btn btn-danger" onclick="${onLogout}()">Logout</button></li>
                </ul>
            </div>
            <div id="user-logged-out" class="dropdown d-none">
                <button class="btn dropdown-toggle navbar-dropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <span id="user-full-name">Anonimo</span>
                </button>
                <ul class="dropdown-menu">
                    <!--<li><button class="dropdown-item" onclick="${onLogin}()">Login</button></li>-->
                    <li><a href="/static/login/login.html" role="button" class="dropdown-item">Login</a></li>
                </ul>
            </div>
        </div>`;
    document.getElementById(containerId).innerHTML = navbar;
}

function updateNavbar(user) {
    const userProfileAvatar = document.getElementById('user-avatar');
    const userProfileDropdown = document.getElementById('user-full-name');
    const userProfileDropdownLoggedIn = document.getElementById('user-logged-in');
    const userProfileDropdownLoggedOut = document.getElementById('user-logged-out');
    if (user.id) {
        userProfileAvatar.classList.remove('d-none');
        userProfileDropdown.innerText = user.fullName;
        userProfileDropdownLoggedIn.classList.remove('d-none');
        userProfileDropdownLoggedOut.classList.add('d-none');
    } else {
        userProfileAvatar.classList.add('d-none');
        userProfileDropdown.innerText = 'Anonimo';
        userProfileDropdownLoggedIn.classList.add('d-none');
        userProfileDropdownLoggedOut.classList.remove('d-none');
    }
}

window.onpageshow = function() {
    const user = LoginManager.getUser();
    updateNavbar(user);
    console.log('navbar:onpageshow');
};