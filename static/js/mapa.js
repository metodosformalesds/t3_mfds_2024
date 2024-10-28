// Inicializar el mapa centrado provisionalmente en Cd. Juárez
var map = L.map('map').setView([31.6904, -106.4245], 13);

// Cargar el mapa desde OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variables para almacenar la ubicación del usuario y la capa de la ruta
let userLat = null;
let userLng = null;
let routeLayer = null;  // Capa para mostrar la ruta

// Intentar obtener la ubicación del usuario
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
        function (position) {
            userLat = position.coords.latitude;
            userLng = position.coords.longitude;

            // Centrar el mapa en la ubicación del usuario
            map.setView([userLat, userLng], 13);

            // Agregar un marcador en la ubicación del usuario
            L.marker([userLat, userLng])
                .addTo(map)
                .bindPopup("Estás aquí.")
                .openPopup();
        },
        function () {
            console.error("No se pudo obtener la ubicación.");
        }
    );
} else {
    console.error("Geolocalización no soportada en este navegador.");
}

// Obtener los Yonkes de la API
fetch('/api/yonkes/')
    .then(response => response.json())
    .then(yonkes => {
        yonkes.forEach(yonke => {
            const marker = L.marker([yonke.latitud, yonke.longitud]).addTo(map);

            // Crear un popup con información del Yonke y un botón para ver la ruta
            const popupContent = `
                <strong>${yonke.nombre}</strong><br>
                ${yonke.direccion}<br>
                <button onclick="trazarRuta(${yonke.latitud}, ${yonke.longitud})" class="btn btn-sm btn-primary mt-2">
                    Ver ruta
                </button>
            `;
            marker.bindPopup(popupContent);
        });
    })
    .catch(error => console.error('Error al cargar los yonkes:', error));

// Función para trazar la ruta con OSRM
function trazarRuta(destLat, destLng) {
    if (userLat !== null && userLng !== null) {
        // URL de la API de OSRM para calcular la ruta
        const url = `https://router.project-osrm.org/route/v1/driving/${userLng},${userLat};${destLng},${destLat}?overview=full&geometries=geojson`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Si ya hay una ruta en el mapa, la eliminamos
                if (routeLayer) {
                    map.removeLayer(routeLayer);
                }

                // Dibujar la nueva ruta en el mapa
                const routeCoordinates = data.routes[0].geometry.coordinates.map(coord => [coord[1], coord[0]]);
                routeLayer = L.polyline(routeCoordinates, { color: 'blue', weight: 5 }).addTo(map);

                // Ajustar el zoom para mostrar toda la ruta
                map.fitBounds(routeLayer.getBounds());
            })
            .catch(error => console.error('Error al calcular la ruta:', error));
    } else {
        alert("No se pudo obtener tu ubicación. Por favor, permite el acceso a tu ubicación.");
    }
}
