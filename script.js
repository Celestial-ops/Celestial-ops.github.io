// Your Discord Webhook URL
const DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1467137149873819710/oDpNM0_05l4BLYpA6yri4jQ_mB14fvJF5wkOOsMozD4KNM17kBXFmb189GWvxr2-r_kb";

async function trackPlayer() {
    const username = document.getElementById('username').value;
    const resultDiv = document.getElementById('result');
    const statusDiv = document.getElementById('status');
    const lobbyDiv = document.getElementById('lobbyCode');

    if (!username) return alert("Please enter a username");

    resultDiv.style.display = 'block';
    statusDiv.innerHTML = "Searching...";
    lobbyDiv.innerHTML = "";

    try {
        // API Endpoint for Animal Company (Nakama)
        const apiUrl = `https://animalcompany.us-east1.nakamacloud.io:443/v2/rpc/get_player_status`;
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer defaultkey' // This may need the actual game client key
            },
            body: JSON.stringify({ username: username })
        });

        const data = await response.json();

        if (data.payload) {
            const info = JSON.parse(data.payload);
            const lobbyCode = info.room_id || "Private/In-Game";
            
            if (info.is_online) {
                statusDiv.innerHTML = `<span class="online">ONLINE</span>`;
                lobbyDiv.innerHTML = `Lobby Code: ${lobbyCode}`;
                
                // Trigger the Discord Webhook
                sendToDiscord(username, lobbyCode, "Online");
            } else {
                statusDiv.innerHTML = `<span class="offline">OFFLINE</span>`;
                sendToDiscord(username, "N/A", "Offline");
            }
        } else {
            statusDiv.innerHTML = "User not found.";
        }
    } catch (error) {
        statusDiv.innerHTML = "Error connecting to API.";
    }
}

// Function to send data to Discord
async function sendToDiscord(user, code, status) {
    const payload = {
        "content": null,
        "embeds": [
            {
                "title": "🎯 Player Tracked!",
                "color": status === "Online" ? 5763719 : 15548997, // Green for online, Red for offline
                "fields": [
                    { "name": "Username", "value": `\`${user}\``, "inline": true },
                    { "name": "Status", "value": status, "inline": true },
                    { "name": "Lobby Code", "value": `**${code}**`, "inline": false }
                ],
                "footer": { "text": "Animal Company Tracker" },
                "timestamp": new Date().toISOString()
            }
        ]
    };

    try {
        await fetch(DISCORD_WEBHOOK_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch (err) {
        console.error("Discord Webhook Error:", err);
    }
}
