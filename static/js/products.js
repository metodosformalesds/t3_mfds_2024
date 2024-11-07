async function cargarProductos() {
    const productContainer = document.getElementById('product-container');

    try {
        // Cambia la URL a la correcta para obtener productos de la API
        const responseApi = await fetch('http://localhost:3000/autopartes');
        
        // Verifica si la respuesta fue exitosa
        if (!responseApi.ok) {
            throw new Error(`Error al obtener los productos de la API: ${responseApi.status}`);
        }

        // Obtiene la lista de productos
        const productos = await responseApi.json();

        // Limpia el contenedor antes de cargar los productos
        productContainer.innerHTML = '';

        // Verifica si hay productos
        if (productos.length === 0) {
            productContainer.innerHTML = '<p>No hay productos disponibles en este momento.</p>';
            return;
        }

        // Itera sobre los productos y crea el HTML para cada uno
        productos.forEach(producto => {
            const productHTML = `
                <div class="col-4">
                    <a href="/producto/${producto.id}/"><img src="${producto.imagen}" alt="${producto.titulo}"></a>
                    <h4>${producto.titulo}</h4>
                    <div class="rating">
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star"></i>
                        <i class="fa fa-star-o"></i>
                    </div>
                    <p>$${producto.precio}</p>
                </div>
            `;
            // Inserta el producto en el contenedor
            productContainer.insertAdjacentHTML('beforeend', productHTML);
        });

    } catch (error) {
        console.error('Error al cargar los productos:', error);

        // Solo muestra el mensaje de error si no hay productos en el contenedor
        if (productContainer.innerHTML.trim() === '') {
            productContainer.innerHTML = '<p style="color: red;">Hubo un error al cargar los productos. Intenta nuevamente más tarde.</p>';
        }
    }
}

// Llamada para cargar productos cuando la página esté lista
document.addEventListener("DOMContentLoaded", cargarProductos);
