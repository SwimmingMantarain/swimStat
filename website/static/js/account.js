function deleteAccount(user) {
    console.log(user)
    fetch("/delete-account", {
        method: "POST",
        body: JSON.stringify({ accountId: accountId })
    }).then((_res) => {
        window.location.href = "/";
    });
}