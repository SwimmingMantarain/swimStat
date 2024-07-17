async function deleteAccount(user) {
    const response = await fetch("/delete-account", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}