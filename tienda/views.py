from django.shortcuts import get_object_or_404, render

from tienda.models import Producto

def index(request):
    return render(request, 'tienda/index.html')

def catalogo(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'tienda/catalogo.html', {'productos': productos})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Obtener un producto específico
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})
