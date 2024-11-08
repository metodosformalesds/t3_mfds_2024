let currentPage = 1;
const itemsPerPage = 8;

async function cargarProductos() {
    const productContainer = document.getElementById('product-container');

    try {
        // Obtener los productos desde productos.json
        const response = await fetch('/static/js/productos.json');
        
        if (!response.ok) {
            throw new Error('No se pudo cargar el archivo productos.json');
        }

        const productos = await response.json();

        // Mostrar los productos por página
        mostrarProductosPorPagina(productos, currentPage);

        // Configurar paginación
        configurarPaginacion(productos);

    } catch (error) {
        console.error('Error al cargar los productos desde productos.json:', error);
        productContainer.innerHTML = '<p style="color: red;">Hubo un error al cargar los productos. Intenta nuevamente más tarde.</p>';
    }
}

function mostrarProductosPorPagina(productos, page) {
    const productContainer = document.getElementById('product-container');
    productContainer.innerHTML = '';

    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const productosPagina = productos.slice(startIndex, endIndex);

    productosPagina.forEach(producto => {
        const productHTML = `
            <div class="col-4">
                <a href="/producto/${producto.id}/">
                    <img src="${producto.imagen}" alt="${producto.titulo}">
                </a>
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
        productContainer.insertAdjacentHTML('beforeend', productHTML);
    });
}

function configurarPaginacion(productos) {
    const totalPages = Math.ceil(productos.length / itemsPerPage);
    const pageContainer = document.querySelector('.page-btn');
    pageContainer.innerHTML = ''; // Limpiar botones de paginación previos

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('span');
        pageButton.innerText = i;
        pageButton.classList.add('page-button');
        if (i === currentPage) {
            pageButton.classList.add('active');
        }

        pageButton.addEventListener('click', () => {
            currentPage = i;
            mostrarProductosPorPagina(productos, currentPage);
            configurarPaginacion(productos);
        });

        pageContainer.appendChild(pageButton);
    }

    // Agregar botón siguiente (→)
    if (totalPages > 1) {
        const nextButton = document.createElement('span');
        nextButton.innerHTML = '&#8594;';
        nextButton.classList.add('next-button');

        nextButton.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                mostrarProductosPorPagina(productos, currentPage);
                configurarPaginacion(productos);
            }
        });

        pageContainer.appendChild(nextButton);
    }
}

// Llamada para cargar productos cuando la página esté lista
document.addEventListener("DOMContentLoaded", cargarProductos);
