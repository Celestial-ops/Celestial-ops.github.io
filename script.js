const DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb";

async function trackPlayer() {
    const user = document.getElementById('username').value;
    const statusText = document.getElementById('status-text');
    const statusDot = document.getElementById('status-dot');
    const lobbyDisplay = document.getElementById('lobbyCode');

    if (!user) return;

    statusText.innerText = "TRACKING...";
    statusDot.className = ""; // Reset classes

    try {
        const response = await fetch(`https://animalcompany.us-east1.nakamacloud.io:443/v2/rpc/get_player_status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer defaultkey' },
            body: JSON.stringify({ username: user })
        });

        const data = await response.json();
        const info = JSON.parse(data.payload);

        if (info.is_online) {
            statusText.innerText = "ONLINE";
            statusDot.classList.add('online-dot');
            lobbyDisplay.innerText = info.room_id || "HIDDEN";
            sendToDiscord(user, info.room_id || "HIDDEN", "Online");
        } else {
            statusText.innerText = "OFFLINE";
            statusDot.classList.add('offline-dot');
            lobbyDisplay.innerText = "----";
            sendToDiscord(user, "N/A", "Offline");
        }
    } catch (e) {
        statusText.innerText = "API ERROR";
        lobbyDisplay.innerText = "ERROR";
    }
}

// ... include the same sendToDiscord function from the previous step ...
