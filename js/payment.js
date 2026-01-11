function sendReservation() {
    fetch("http://localhost:8000/reserve", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            fullname: fullname,
            email: email,
            langage: langage,
            pack: pack
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            window.location.href = "confirmation.html";
        }
    });
}