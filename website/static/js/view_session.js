async function deleteSession(sessionID) {
    await fetch("delete-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sessionID: sessionID })
    })
    window.location.href = "/view_sessions";
}