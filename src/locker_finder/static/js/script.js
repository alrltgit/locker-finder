API_URL="https://like-truth-closure-boss.trycloudflare.com";
LOCKER_URL=`${API_URL}/api/all/lockers`;

var map = L.map('map').setView([51.9194, 19.1451], 6);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let FALLBACK_LAT = 52.2297;
let FALLBACK_LON = 21.0122;

const cachedLat = sessionStorage.getItem("user_lat");
const cachedLon = sessionStorage.getItem("user_lon")

let markerClusterGroup = L.markerClusterGroup({
    maxClusterRadius: 150,
    chunkedLoading: true,
    chunkSize: 200,
    chunkDelay: 50
});
map.addLayer(markerClusterGroup);

if (cachedLat && cachedLon) {
    loadMap(parseFloat(cachedLat), parseFloat(cachedLon))
} else if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const user_lat = position.coords.latitude;
            const user_lon = position.coords.longitude;

            sessionStorage.setItem("user_lat", user_lat);
            sessionStorage.setItem("user_lon", user_lon);

            loadMap(user_lat, user_lon);
        },
        (error) => {
            console.warn("Geolocation failed, using fallback:", error.message);
            showLocationNotice();
            loadMap(FALLBACK_LAT, FALLBACK_LON); // ← use fallback
        },
        { timeout: 10000, maximumAge: 60000 }
    );
} else {
    showLocationNotice();
    loadMap(FALLBACK_LAT, FALLBACK_LON);
}

function loadMap(lat, lon) {
    map.setView([lat, lon], 13);
    fetchNearestLockers(lat, lon);
}

document.getElementById("options").addEventListener("change", function() {
    const mode = this.value;
    const lat = parseFloat(sessionStorage.getItem("user_lat")) || FALLBACK_LAT
    const lon = parseFloat(sessionStorage.getItem("user_lon")) || FALLBACK_LON

    if (mode == "nearest") {
        fetchNearestLockers(lat, lon);
    } else if (mode == "all") {
        fetchAllLockers();
    }
})

function renderLockers(data) {
    markerClusterGroup.clearLayers();

    const markers = []
    data.forEach(locker => {
        if (locker.lat && locker.lon) {
            const marker = L.marker([locker.lat, locker.lon])
                .bindPopup(() => formLockerInfo(locker));
            markers.push(marker);
        }
    });
    markerClusterGroup.addLayers(markers);
}

function fetchAllLockers() {
    fetch(LOCKER_URL)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) return;
            renderLockers(data);
        })
        .catch(err => console.error("Failed to fetch lockers:", err));
}

function fetchNearestLockers(lat, lon) {
    fetch(`${API_URL}/api/lockers/nearest?lat=${lat}&lon=${lon}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) return;
            renderLockers(data);
        })
        .catch(err => console.error("Failed to fetch lockers:", err));
}

function formLockerInfo(locker) {
    const lockerInfo = `
        <div class="locker-popup">
            <h3>${locker.name}</h3>
            <p><strong>Address:</strong> ${locker.address_line1}, ${locker.address_line2}</p>
            <p><strong>Opening hours:</strong> ${locker.open_hours ?? "24/7"}</p>
            <p><strong>Status:</strong> ${locker.status}</p>
            <a href="https://www.google.com/maps?q=${locker.lat},${locker.lon}" target="_blank">
                Open in Google Maps
            </a>
        </div>
    `;
    return lockerInfo;
}

function showLocationNotice(error) {
    alert("Location access was denied. Showing results for Warsaw. Enable location in your browser");
}
