document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';

    // Get form data
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Hide loading
        document.getElementById('loading').style.display = 'none';

        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        // Display result
        displayResult(data);

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Error making prediction: ' + error.message);
    }
});

async function lookupFlight() {
    const flightNumber = document.getElementById('flightNumber').value.trim();
    const resultDiv = document.getElementById('lookupResult');

    if (!flightNumber) {
        resultDiv.innerHTML = '<p class="error">Please enter a flight number</p>';
        return;
    }

    resultDiv.innerHTML = '<p class="loading-text">Looking up flight...</p>';

    try {
        const response = await fetch('/lookup-flight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ flight_number: flightNumber })
        });

        const data = await response.json();

        if (data.found) {
            // Auto-fill form
            document.getElementById('airline').value = data.airline;
            document.getElementById('origin').value = data.origin;
            document.getElementById('destination').value = data.destination;

            // Show success message
            resultDiv.innerHTML = `
                <div class="lookup-success">
                    <p style="margin-bottom: 0.25rem;"><i class="fa-solid fa-circle-check"></i> Flight Profile Identified</p>
                    <p style="font-size: 1.1rem; font-weight: 700;">${data.airline_name} <span style="font-weight: 400; color: var(--text-muted)">| Flight ${data.flight_number}</span></p>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-map-location-dot"></i> ${data.origin_name} (${data.origin}) &rarr; ${data.destination_name} (${data.destination})</p>
                    <div class="status-badge"><i class="fa-solid fa-satellite-dish"></i> Status: ${data.status}</div>
                    ${data.source === 'demo' ? '<p class="demo-note" style="margin-top: 0.5rem; font-size: 0.8rem; color: #f59e0b;"><i class="fa-solid fa-triangle-exclamation"></i> Using demo data matrix</p>' : ''}
                </div>
            `;

            // Scroll to form
            document.getElementById('predictionForm').scrollIntoView({ behavior: 'smooth' });
        } else {
            resultDiv.innerHTML = `
                <div class="lookup-error">
                    <p><i class="fa-solid fa-circle-xmark"></i> ${data.error}</p>
                    ${data.available_demos ? `<p style="font-size: 0.85rem; margin-top: 0.5rem;"><i class="fa-solid fa-lightbulb"></i> Try demo flights: ${data.available_demos.join(', ')}</p>` : ''}
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="error"><i class="fa-solid fa-triangle-exclamation"></i> Error: ${error.message}</p>`;
    }
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');

    const statusClass = data.prediction === 1 ? 'delayed' : 'ontime';
    const statusIcon = data.prediction === 1 ? 'fa-clock-rotate-left' : 'fa-plane-departure';

    let historyHTML = '';
    if (data.route_history) {
        historyHTML = `
            <div class="route-history">
                <h3 class="section-title"><i class="fa-solid fa-chart-line" style="color: var(--primary)"></i> Route History Diagnostics</h3>
                <div class="history-stats">
                    <div class="stat-item">
                        <span class="label">Total Flights</span>
                        <span class="val">${data.route_history.total_flights}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">Avg Delay</span>
                        <span class="val">${data.route_history.avg_delay.toFixed(1)}m</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">On-Time Rate</span>
                        <span class="val">${data.route_history.on_time_rate.toFixed(1)}%</span>
                    </div>
                </div>
            </div>
        `;
    }

    let alternativesHTML = '';
    if (data.alternatives && data.alternatives.length > 0) {
        alternativesHTML = `
            <div class="alternatives">
                <h3 class="section-title"><i class="fa-solid fa-code-branch" style="color: var(--warning)"></i> Optimal Alternatives (Lower Risk)</h3>
                <ul>
                    ${data.alternatives.map(alt => `
                        <li><i class="fa-solid fa-plane"></i> <span>${alt.route}</span> <span style="margin-left: auto; color: var(--text-muted); font-size: 0.85rem">${alt.total_distance} miles</span></li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    resultContent.innerHTML = `
        <div class="prediction-result">
            <h3 class="section-title" style="justify-content: center; margin-bottom: 1.5rem;"><i class="fa-solid fa-microchip"></i> ML Prediction Result</h3>
            <div class="probability-circle" style="border-color: ${data.risk_color}; color: ${data.risk_color}">
                <span>${data.probability.toFixed(1)}<span style="font-size: 1.5rem">%</span></span>
            </div>
            <div class="status ${statusClass}">
                <i class="fa-solid ${statusIcon}"></i> ${data.status}
            </div>
            <div class="risk-badge" style="background-color: ${data.risk_color};">
                <i class="fa-solid fa-shield-halved"></i> Risk Level: ${data.risk_level}
            </div>
            
            <div class="meta-stats">
                <span><i class="fa-solid fa-bullseye"></i> Confidence: ${data.confidence.toFixed(1)}%</span>
                <span><i class="fa-solid fa-ruler"></i> Distance: ${data.distance} mi</span>
                <span><i class="fa-regular fa-clock"></i> Eval Time: ${data.current_time}</span>
            </div>
        </div>
        
        ${historyHTML}
        ${alternativesHTML}
        
        <div class="weather-info">
            <h3 class="section-title"><i class="fa-solid fa-cloud-sun" style="color: #38bdf8"></i> Real-time Telemetry (Origin)</h3>
            <div class="weather-grid">
                <div class="weather-item">
                    <i class="fa-solid fa-temperature-half"></i>
                    <strong>Temp</strong>
                    <span>${data.weather.temperature.toFixed(1)}°C</span>
                </div>
                <div class="weather-item">
                    <i class="fa-solid fa-droplet"></i>
                    <strong>Humidity</strong>
                    <span>${data.weather.humidity}%</span>
                </div>
                <div class="weather-item">
                    <i class="fa-solid fa-wind"></i>
                    <strong>Wind</strong>
                    <span>${data.weather.wind_speed.toFixed(1)} m/s</span>
                </div>
                <div class="weather-item">
                    <i class="fa-regular fa-eye"></i>
                    <strong>Vis</strong>
                    <span>${(data.weather.visibility / 1000).toFixed(1)} km</span>
                </div>
                <div class="weather-item">
                    <i class="fa-solid fa-gauge-high"></i>
                    <strong>Press</strong>
                    <span>${data.weather.pressure} hPa</span>
                </div>
                <div class="weather-item">
                    <i class="fa-solid fa-bolt"></i>
                    <strong>Severity</strong>
                    <span>${data.weather.weather_severity}/10</span>
                </div>
            </div>
        </div>
    `;

    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}
