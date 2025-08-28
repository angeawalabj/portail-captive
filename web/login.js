document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8000/portal/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({username, password})
    });

    const messageDiv = document.getElementById("message");

    if (response.ok) {
        window.location.href = "welcome.html";
    } else {
        const data = await response.json();
        messageDiv.textContent = data.detail || "Erreur de connexion";
    }
});
