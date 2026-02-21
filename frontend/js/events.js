fetch("http://127.0.0.1:8000/api/events/")
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("events");

        data.events.forEach((event, index) => {
            const card = document.createElement("div");
            card.className = "event-card";
            card.style.animationDelay = `${index * 0.1}s`;

            card.innerHTML = `
                <h3>${event.title}</h3>
                <p><strong>Date:</strong> ${event.date_time}</p>
                <p><strong>City:</strong> ${event.city}</p>
                <p><strong>Source:</strong> ${event.source}</p>
                <button onclick="getTickets(${event.id})">GET TICKETS</button>
            `;

            container.appendChild(card);
        });
    });

function getTickets(eventId) {
    const email = prompt("Enter your email to continue:");
    if (!email) return;

    fetch("http://127.0.0.1:8000/api/get-tickets/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email,
            consent: true,
            event_id: eventId
        })
    })
    .then(res => res.json())
    .then(data => {
        window.location.href = data.redirect_url;
    });
}