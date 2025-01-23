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
                    <!--<div id="user-avatar" class="rounded-circle user-avatar"></div>-->
                    <i id="user-avatar" class="user-avatar bi bi-person-circle"></i>
                    <span id="user-full-name">Nome utente</span>
                </button>
                <ul class="dropdown-menu">
                  <!--<li><a class="dropdown-item">Profilo</a></li>
                    <li><hr class="dropdown-divider"></li>-->
                    <li>
                        <button class="dropdown-item btn btn-danger text-danger" onclick="${onLogout}()">
                            <i class="bi bi-box-arrow-left"></i>
                            Logout
                        </button>
                    </li>
                </ul>
            </div>
            <div id="user-logged-out" class="dropdown d-none">
                <button class="btn dropdown-toggle navbar-dropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <i id="user-avatar-anonymous" class="user-avatar bi bi-incognito"></i>
                    <span id="user-full-name">Anonimo</span>
                </button>
                <ul class="dropdown-menu">
                    <!--<li><button class="dropdown-item" onclick="${onLogin}()">Login</button></li>-->
                    <li>
                        <a href="/static/login/login.html" role="button" class="dropdown-item">
                            <i class="bi bi-box-arrow-right"></i>
                            Login
                        </a>
                    </li>
                </ul>
            </div>
        </div>`;
    document.getElementById(containerId).innerHTML = navbar;
}

function updateNavbar(user) {
    const userProfileDropdown = document.getElementById('user-full-name');
    const userProfileDropdownLoggedIn = document.getElementById('user-logged-in');
    const userProfileDropdownLoggedOut = document.getElementById('user-logged-out');
    if (user.id) {
        userProfileDropdown.innerText = user.fullName;
        userProfileDropdownLoggedIn.classList.remove('d-none');
        userProfileDropdownLoggedOut.classList.add('d-none');
    } else {
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