async function deleteAccount(user) {
    const response = await fetch("/delete-account", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}

async function deleteSessions(user) {
    const response = await fetch("/delete-sessions", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}