function deleteAccount(user) {
    console.log(user)
    fetch("/delete-account", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}