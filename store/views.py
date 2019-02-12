from django.shortcuts import render, redirect
from .models import Product
# Create your views here.

def catalog(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    cart = request.session['cart']
    request.session.set_expiry(0)    
    store_items = Product.objects.all()
    ctx = {'store_items': store_items, 'cart_items': len(cart)}
    if request.method == "POST":
        cart.append(int(resquest.POST['obj_id']))
        return redirect('catalog')

    return render (request, "catalog.html", ctx)


