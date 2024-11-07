const express = require('express');
const axios = require('axios');
const cors = require('cors');
const crypto = require('crypto');
const readline = require('readline');

const app = express();
const PORT = process.env.PORT || 3000;

// Credenciales de Mercado Libre
const CLIENT_ID = "3314572772087149";
const CLIENT_SECRET = "C9Qpn9keSD30k2eopH1telVuRG4yV4Tn";
const REDIRECT_URI = "https://horuz.me";

// Variables para almacenar el token temporalmente
let accessToken = "";
let refreshToken = "";
let expiresIn = 21600;
let tokenObtainedTime = Date.now();

// Habilita CORS para permitir solicitudes desde cualquier origen
app.use(cors());
app.use(express.json()); // Middleware para interpretar JSON

// Función para generar el `code_verifier` y el `code_challenge` para PKCE
function generateCodeVerifierAndChallenge() {
    const codeVerifier = crypto.randomBytes(32).toString('base64url');
    const codeChallenge = crypto.createHash('sha256').update(codeVerifier).digest('base64url');
    return { codeVerifier, codeChallenge };
}

// Genera el code_verifier y code_challenge al inicio del servidor
const { codeVerifier, codeChallenge } = generateCodeVerifierAndChallenge();

// Función para verificar si el token ha expirado
function isTokenExpired() {
    const currentTime = Date.now();
    return currentTime - tokenObtainedTime >= expiresIn * 1000;
}

// Función para obtener un nuevo token de acceso usando `refresh_token`
async function refreshAccessToken() {
    try {
        const response = await axios.post('https://api.mercadolibre.com/oauth/token', {
            grant_type: 'refresh_token',
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            refresh_token: refreshToken
        });
        accessToken = response.data.access_token;
        refreshToken = response.data.refresh_token;
        expiresIn = response.data.expires_in;
        tokenObtainedTime = Date.now();

        console.log("Nuevo access_token obtenido automáticamente:", accessToken);
    } catch (error) {
        console.error("Error al refrescar el access_token:", error.response ? error.response.data : error.message);
    }
}

// Función para obtener el token inicial usando el `auth_code` y `code_verifier`
async function getInitialAccessToken(authCode) {
    try {
        const response = await axios.post('https://api.mercadolibre.com/oauth/token', {
            grant_type: 'authorization_code',
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            code: authCode,
            redirect_uri: REDIRECT_URI,
            code_verifier: codeVerifier
        });
        accessToken = response.data.access_token;
        refreshToken = response.data.refresh_token;
        expiresIn = response.data.expires_in;
        tokenObtainedTime = Date.now();

        console.log("Token inicial obtenido:", accessToken);
    } catch (error) {
        console.error("Error al obtener el token inicial:", error.response ? error.response.data : error.message);
    }
}

// Configura el readline para recibir input del usuario
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Pregunta al usuario el auth_code
console.log("Visita la siguiente URL para autorizar la aplicación:");
console.log(`https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&code_challenge=${codeChallenge}&code_challenge_method=S256`);
rl.question('Ingresa el auth_code proporcionado por Mercado Libre: ', (authCode) => {
    getInitialAccessToken(authCode).then(() => {
        rl.close();
        app.listen(PORT, '3.23.224.207', () => {
            console.log(`Servidor escuchando en el puerto ${PORT}`);
        });
    }).catch(error => {
        console.error("Error al obtener el token inicial:", error);
        rl.close();
    });
});

// Función que verifica y renueva el token si es necesario antes de cada solicitud
async function ensureValidAccessToken() {
    if (isTokenExpired()) {
        console.log("El token ha expirado. Intentando refrescar...");
        await refreshAccessToken();
    } else {
        console.log("El token aún es válido.");
    }
}

// Función para obtener productos de autopartes con imágenes en alta resolución
async function getAutoParts() {
    await ensureValidAccessToken();
    try {
        const response = await axios.get('https://api.mercadolibre.com/sites/MLM/search', {
            params: { category: 'MLM1747', limit: 10 },
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        const productos = await Promise.all(response.data.results.map(async producto => {
            const detalleProducto = await axios.get(`https://api.mercadolibre.com/items/${producto.id}`, {
                headers: { Authorization: `Bearer ${accessToken}` }
            });
            const imagenAltaResolucion = detalleProducto.data.pictures.length > 0 ? detalleProducto.data.pictures[0].url : producto.thumbnail;

            return {
                id: producto.id,
                titulo: producto.title,
                precio: producto.price,
                imagen: imagenAltaResolucion,
                link: producto.permalink
            };
        }));

        return productos;
    } catch (error) {
        console.error("Error al obtener productos:", error.response ? error.response.data : error.message);
        return [];
    }
}

// Ruta para obtener productos de autopartes
app.get('/autopartes', async (req, res) => {
    const productos = await getAutoParts();
    res.json(productos);
});

// Nueva ruta para obtener los detalles de un producto específico por ID
app.get('/productos/:id', async (req, res) => {
    const productId = req.params.id;
    await ensureValidAccessToken();

    try {
        const response = await axios.get(`https://api.mercadolibre.com/items/${productId}`, {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        // Obtener descripción detallada
        const descripcionResponse = await axios.get(`https://api.mercadolibre.com/items/${productId}/description`, {
            headers: { Authorization: `Bearer ${accessToken}` }
        });

        // Enviar los datos detallados del producto
        res.json({
            id: response.data.id,
            titulo: response.data.title,
            precio: response.data.price,
            descripcion: descripcionResponse.data.plain_text || "Descripción no disponible",
            imagen: response.data.pictures[0]?.url || "", // Imagen principal
            pictures: response.data.pictures // Array de imágenes adicionales
        });
    } catch (error) {
        console.error("Error al obtener detalles del producto:", error);
        res.status(500).json({ error: 'Error al obtener los detalles del producto' });
    }
});
