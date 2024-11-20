let currentPage = 1;
const itemsPerPage = 8;
let productos = []; // Variable para almacenar todos los productos cargados

async function cargarProductos() {
    const productContainer = document.getElementById('product-container');

    try {
        // Obtener los productos desde productos.json
        const response = await fetch('/static/js/productos.json');
        
        if (!response.ok) {
            throw new Error('No se pudo cargar el archivo productos.json');
        }

        productos = await response.json();

        // Mostrar los productos por página (todos los productos por defecto)
        mostrarProductosPorPagina(productos, currentPage);

        // Configurar paginación
        configurarPaginacion(productos);

        // Configurar el evento de ordenamiento por precio
        configurarOrdenarPorPrecio();

    } catch (error) {
        console.error('Error al cargar los productos desde productos.json:', error);
        productContainer.innerHTML = '<p style="color: red;">Hubo un error al cargar los productos. Intenta nuevamente más tarde.</p>';
    }
}

function mostrarProductosPorPagina(productosFiltrados, page) {
    const productContainer = document.getElementById('product-container');
    productContainer.innerHTML = '';

    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const productosPagina = productosFiltrados.slice(startIndex, endIndex);

    if (productosPagina.length === 0) {
        productContainer.innerHTML = '<p>No hay productos disponibles.</p>';
    } else {
        productosPagina.forEach(producto => {
            const productHTML = `
                <div class="col-4">
                    <a href="/producto/${producto.id}/">
                        <img src="${producto.imagen}" alt="${producto.titulo}" class="product-img">
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
}

function configurarPaginacion(productosFiltrados) {
    const totalPages = Math.ceil(productosFiltrados.length / itemsPerPage);
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
            cambiarPagina(i, productosFiltrados);
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
                cambiarPagina(currentPage + 1, productosFiltrados);
            }
        });

        pageContainer.appendChild(nextButton);
    }
}

function cambiarPagina(nuevaPagina, productosFiltrados) {
    currentPage = nuevaPagina;
    mostrarProductosPorPagina(productosFiltrados, currentPage);
    configurarPaginacion(productosFiltrados);
}

function configurarOrdenarPorPrecio() {
    const ordenarPrecioSelect = document.getElementById('ordenarPrecio');

    ordenarPrecioSelect.addEventListener('change', () => {
        const ordenSeleccionado = ordenarPrecioSelect.value;

        let productosOrdenados = [...productos];

        switch (ordenSeleccionado) {
            case 'precio-asc':
                productosOrdenados.sort((a, b) => a.precio - b.precio);
                break;
            case 'precio-desc':
                productosOrdenados.sort((a, b) => b.precio - a.precio);
                break;
            default:
                productosOrdenados = [...productos];
                break;
        }

        currentPage = 1; // Reinicia a la primera página al ordenar
        mostrarProductosPorPagina(productosOrdenados, currentPage);
        configurarPaginacion(productosOrdenados);
    });
}

// Llamada para cargar productos cuando la página esté lista
document.addEventListener("DOMContentLoaded", cargarProductos);
