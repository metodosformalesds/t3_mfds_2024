document.addEventListener("DOMContentLoaded", function () {
    // Función para alternar el menú en dispositivos móviles
    var MenuItems = document.getElementById("MenuItems");
    MenuItems.style.maxHeight = "0px";
    function menutoggle() {
        if (MenuItems.style.maxHeight == "0px") {
            MenuItems.style.maxHeight = "200px";
        } else {
            MenuItems.style.maxHeight = "0px";
        }
    }

    // Función para cargar los productos desde el backend y mostrarlos en el contenedor
    async function cargarProductos() {
        try {
            // Realiza una solicitud GET a la ruta de productos de tu backend
            const response = await fetch('/api/yonkes/');
            if (!response.ok) {
                throw new Error(`Error al obtener los productos: ${response.status}`);
            }
            const productos = await response.json();

            // Selecciona el contenedor de productos
            const productContainer = document.getElementById('product-container');
            productContainer.innerHTML = ''; // Limpia el contenedor antes de cargar los productos

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
            const productContainer = document.getElementById('product-container');
            productContainer.innerHTML = '<p>Hubo un error al cargar los productos. Intenta nuevamente más tarde.</p>';
        }
    }

    // Llama a la función para cargar los productos al cargar la página
    cargarProductos();
});
