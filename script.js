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
        // API Endpoint for Nakama systems
        // Note: Nakama usually requires an Authorization header with a 'Server Key'
        const apiUrl = `https://animalcompany.us-east1.nakamacloud.io:443/v2/rpc/get_player_status`;
        
        // This is a hypothetical RPC call. Most games use RPCs to find friends/players.
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer defaultkey' // This key might vary
            },
            body: JSON.stringify({ username: username })
        });

        const data = await response.json();

        if (data.payload) {
            const info = JSON.parse(data.payload);
            
            if (info.is_online) {
                statusDiv.innerHTML = `<span class="online">ONLINE</span>`;
                lobbyDiv.innerHTML = `Lobby Code: ${info.room_id || "Private/In-Game"}`;
            } else {
                statusDiv.innerHTML = `<span class="offline">OFFLINE</span>`;
                lobbyDiv.innerHTML = "";
            }
        } else {
            statusDiv.innerHTML = "User not found or private.";
        }

    } catch (error) {
        console.error(error);
        statusDiv.innerHTML = "Error connecting to API.";
    }
}
