document.getElementById("scanForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const ip = document.getElementById("ip").value;
    const startPort = document.getElementById("start_port").value;
    const endPort = document.getElementById("end_port").value;

    const response = await fetch("https://your-app-name.herokuapp.com/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip, start_port: parseInt(startPort), end_port: parseInt(endPort) }),
    });
    
    const result = await response.json();
    displayResult(result);
});
document.getElementById("scanForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const ip = document.getElementById("ip").value;
    const startPort = document.getElementById("start_port").value;
    const endPort = document.getElementById("end_port").value;
    const progressBar = document.getElementById("scanProgress");

    progressBar.value = 10;  // Start progress at 10%

    const response = await fetch("https://your-app-name.herokuapp.com/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip, start_port: parseInt(startPort), end_port: parseInt(endPort) }),
    });
    

    progressBar.value = 70;  // Midway progress

    const result = await response.json();
    progressBar.value = 100;  // Complete

    displayResult(result);
});


function displayResult(result) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `
        <h2>Scan Results</h2>
        <p><strong>IP:</strong> ${result.ip}</p>
        <p><strong>Status:</strong> ${result.is_alive ? "Alive" : "Dead"}</p>
        <p><strong>Open Ports:</strong> ${result.open_ports.join(", ")}</p>
        <p><strong>Location:</strong> ${result.location.city}, ${result.location.region}, ${result.location.country}</p>
        <p><strong>ISP:</strong> ${result.location.isp}</p>
    `;
}