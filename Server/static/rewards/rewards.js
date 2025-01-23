"use strict"
const user = LoginManager.getUser();
let modalRef = null;
let modalRewardId = null;
let userPoints = 0;

AppNavbar.initNavbar('navbar-container', 'handleLogin', 'logout');

AppSidenav.initSidenav('sidenav-container');
AppSidenav.setActiveMenu(2);

BottomNavigationBar.initBottomNavigationBar('bottom-navigation-bar', 2);

const rewardsContainer = document.getElementById('rewards');
const redeemedRewardsContainer = document.getElementById('redeemed-rewards');
const redeemedRewardsBlock = document.getElementById('redeemed-rewards-block');

loadData();

async function loadData() {
    redeemedRewardsBlock.classList.add('d-none');
    await loadUserPoints();
    await loadRewards();
    redeemedRewardsBlock.classList.remove('d-none');
    loadRedeemedRewards();
}

async function loadRewards() {
    console.log('Fetching rewards...');
    rewardsContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.classList = 'query-message';
    loadingElem.innerText = 'Caricamento...';
    rewardsContainer.appendChild(loadingElem);
    var url = new URL('http://localhost:5000/rewards');
    url.searchParams.append('userId', user.id)
    const rewards = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
    rewardsContainer.replaceChildren();
    if (!rewards.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessuna attività trovata';
        rewardsContainer.appendChild(noActivitiesElem);
    } else {
        rewards.forEach(reward => {
            let cardContent = `
                <div>
                    <p class="activity-card_title">${reward.description}</p>
                </div>
            `;
            if (user.id) {
                if (userPoints > 0) {
                    cardContent += `
                        <div class="activity-cart_actions">
                            <button class="btn btn-primary" onclick="showReserveActivityModal('${reward.id}')">Riscatta</button>
                        </div>`
                } else {
                    cardContent += `
                        <div>Non hai abbastanza punti</div>`
                }
            }
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded activity-card';
            if (!userPoints) {
                card.classList.add('activity-card_disabled');
            }
            card.innerHTML = cardContent;
            rewardsContainer.appendChild(card);
        });
    }
}

async function loadRedeemedRewards() {
    redeemedRewardsContainer.replaceChildren();
    const loadingElem = document.createElement('p');
    loadingElem.classList = 'query-message';
    loadingElem.innerText = '';
    redeemedRewardsContainer.appendChild(loadingElem);
    var url = new URL('http://localhost:5000/redeemed-rewards');
    url.searchParams.append('userId', user.id)
    const rewards = await fetch(url)
        .then(result => result.json())
        .catch(() => []);
        redeemedRewardsContainer.replaceChildren();
    if (!rewards.length) {
        const noActivitiesElem = document.createElement('p');
        noActivitiesElem.className = 'query-message';
        noActivitiesElem.innerText = 'Nessun premio riscattato';
        redeemedRewardsContainer.appendChild(noActivitiesElem);
    } else {
        const redeemedRewardsContainer = document.getElementById('redeemed-rewards');
        redeemedRewardsContainer.replaceChildren();
        rewards.forEach(reward => {
            let cardContent = `
                <div>
                    <p class="activity-card_title">${reward.description}</p>
                    <p><i class="bi bi-upc-scan"></i> Codice: ${reward.code}</p>
                </div>
            `;
            const card = document.createElement('div');
            card.classList = 'p-3 border rounded activity-card';
            card.innerHTML = cardContent;
            redeemedRewardsContainer.appendChild(card.cloneNode(true));
        });
    }
}

async function loadUserPoints() {
    await new Promise(r => setTimeout(r, 1000));
        var url = new URL('http://localhost:5000/user-points');
        url.searchParams.append('userId', user.id)
    const result = await fetch(url)
        .then(result => result.json())
        .catch(() => null);
    userPoints = result?.points || 0;
    updateInterface();
}

async function showReserveActivityModal(rewardId) {
    // Resetto interfaccia
    document.getElementById('redeem-reward-warning').classList.remove('d-none');
    document.getElementById('redeemed-reward').classList.add('d-none');
    document.getElementById('redeem-reward-cancel-button').classList.remove('d-none');
    document.getElementById('redeem-reward-proceed-button').classList.remove('d-none');
    document.getElementById('redeemed-reward-button').classList.add('d-none');
    const modal = document.getElementById('redeemRewardModal');
    modalRef = new bootstrap.Modal(modal);
    modalRef.show();
    modalRewardId = rewardId;
}

async function redeemReward() {
    // Aggiorno interfaccia
    document.getElementById('redeem-reward-warning').classList.add('d-none');
    document.getElementById('redeemed-reward').classList.remove('d-none');
    const redeemedReward = await fetch('http://localhost:5000/redeem-reward', {
            method: 'POST',
            body: JSON.stringify({
                "rewardId": modalRewardId,
                "userId": user.id,
            }),
        })
        .then(result => result.json())
        .catch(err => null);
    if (redeemedReward) {
        document.getElementById('reward-code').innerText = redeemedReward.code;
        document.getElementById('redeem-reward-cancel-button').classList.add('d-none');
        document.getElementById('redeem-reward-proceed-button').classList.add('d-none');
        document.getElementById('redeemed-reward-button').classList.remove('d-none');
        modalRef = null;
        modalRewardId = null;
        loadData();
    }
}

function logout() {
    LoginManager.logout();
    user.id = null;
    user.fullName = null;
    AppNavbar.updateNavbar(user);
    updateInterface();
    loadData();
}

function updateInterface() {
    if (user.id) {
        document.getElementById('logged-in-info').classList.remove('d-none');
        document.getElementById('anonymous-info').classList.add('d-none');
        document.getElementById('logged-in-info').innerText = `Riscatta i premi che vuoi. Ogni premio costa 1 punto (hai ${userPoints} punti).`;
    } else {
        document.getElementById('anonymous-info').classList.remove('d-none');
        document.getElementById('logged-in-info').classList.add('d-none');
    }
}

window.addEventListener('pageshow', () => {
    const currentUser = LoginManager.getUser();
    if (currentUser.id !== user.id) {
        user.id = currentUser.id;
        user.fullName = currentUser.fullName;
        updateInterface();
        loadData();
    } else {
        updateInterface();
    }
});