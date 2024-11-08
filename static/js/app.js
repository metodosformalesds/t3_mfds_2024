const express = require('express');
const axios = require('axios');
const cors = require('cors');
const crypto = require('crypto');
const readline = require('readline');
const fs = require('fs');

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
        app.listen(PORT, '0.0.0.0', () => {
            console.log(`Servidor escuchando en el puerto ${PORT}`);
            // Descarga y guarda los productos después de iniciar el servidor
            if (!fs.existsSync('productos.json')) {
                getAndSaveProducts();
            } else {
                console.log('Archivo productos.json ya existe, cargando productos...');
                cargarProductosDesdeArchivo();
            }
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

// Función para obtener productos de autopartes con imágenes en alta resolución y guardarlos localmente
async function getAndSaveProducts() {
    await ensureValidAccessToken();
    try {
        const productos = [];

        // Realizamos dos solicitudes con un límite de 50 cada una para obtener 100 productos
        for (let offset = 0; offset < 100; offset += 50) {
            const response = await axios.get('https://api.mercadolibre.com/sites/MLM/search', {
                params: { category: 'MLM1747', limit: 50, offset: offset },
                headers: { Authorization: `Bearer ${accessToken}` }
            });

            const productosParciales = await Promise.all(response.data.results.map(async producto => {
                try {
                    // Intentar obtener los detalles del producto, incluyendo la descripción
                    const detalleProducto = await axios.get(`https://api.mercadolibre.com/items/${producto.id}`, {
                        headers: { Authorization: `Bearer ${accessToken}` }
                    });

                    const descripcionResponse = await axios.get(`https://api.mercadolibre.com/items/${producto.id}/description`, {
                        headers: { Authorization: `Bearer ${accessToken}` }
                    });

                    const imagenAltaResolucion = detalleProducto.data.pictures.length > 0 ? detalleProducto.data.pictures[0].url : producto.thumbnail;

                    return {
                        id: producto.id,
                        titulo: producto.title,
                        precio: producto.price,
                        imagen: imagenAltaResolucion,
                        descripcion: descripcionResponse.data.plain_text || "Descripción no disponible",
                        link: producto.permalink,
                        pictures: detalleProducto.data.pictures // Guardar todas las imágenes adicionales también
                    };
                } catch (error) {
                    console.error(`Error al obtener detalles del producto ${producto.id}:`, error.message);
                    return {
                        id: producto.id,
                        titulo: producto.title,
                        precio: producto.price,
                        imagen: producto.thumbnail,
                        descripcion: "Descripción no disponible",
                        link: producto.permalink,
                        pictures: [] // Si hay un error, no añadimos imágenes adicionales
                    };
                }
            }));

            productos.push(...productosParciales);
        }

        // Guardar los productos en un archivo JSON solo si hay productos
        if (productos.length > 0) {
            fs.writeFileSync('productos.json', JSON.stringify(productos, null, 2));
            console.log("Productos guardados exitosamente en productos.json");
        } else {
            console.error("No se encontraron productos para guardar.");
        }
    } catch (error) {
        console.error("Error al obtener productos:", error.response ? error.response.data : error.message);
    }
}

// Función para cargar productos desde el archivo JSON local
let productos = [];
function cargarProductosDesdeArchivo() {
    try {
        const data = fs.readFileSync('productos.json');
        if (data.length === 0) {
            throw new Error("El archivo productos.json está vacío");
        }
        productos = JSON.parse(data);
        console.log('Productos cargados correctamente desde productos.json');
    } catch (error) {
        console.error('Error al cargar productos desde productos.json:', error.message);
    }
}

// Ruta para obtener productos de autopartes desde el archivo local
app.get('/autopartes', (req, res) => {
    res.json(productos);
});

// Nueva ruta para obtener los detalles de un producto específico por ID
app.get('/productos/:id', (req, res) => {
    const productId = req.params.id;
    const producto = productos.find(p => p.id === productId);

    if (producto) {
        res.json(producto);
    } else {
        res.status(404).json({ error: 'Producto no encontrado' });
    }
});
