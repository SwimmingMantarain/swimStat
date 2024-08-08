async function killTunnel() {
    const response = await fetch("/kill-tunnel", {
        method: "POST",
        body: JSON.stringify({ user: user })
    }).then((_res) => {
        window.location.href = "/";
    });
}