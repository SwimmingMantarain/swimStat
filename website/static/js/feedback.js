async function sendFeedback(data) {
    console.log(data)
    const response = await fetch("/feedback", {
        method: "POST",
        body: JSON.stringify({ data: data })
    }).then((_res) => {
        window.location.href = "/";
    });
}