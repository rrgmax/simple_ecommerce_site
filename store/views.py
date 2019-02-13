from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth import authenticate, login
# Create your views here.
def cartItems(cart):
    items = []
    for item in cart:
        items.append(Product.objects.get(id=int(item)))
    return items

def priceCart(cart):
    cart_items = cartItems(cart)
    price = 0
    for item in cart_items:
        price += item.price
    return price

def genItemsList(cart):
    cart_items = cartItems(cart)
    items_list = ""
    for item in cart_items:
        items_list += ","
        items_list += item.name
    return items_list
def removefromcart(request):
    request.session.set_expiry(0)
    obj_to_remove = request.POST['obj_id']
    obj_indx = request.session['cart'].index(int(obj_to_remove))
    request.session['cart'].pop(obj_indx)
    return redirect("cart")


def catalog(request):
    if 'cart' not in request.session:
        cart = []
        request.session['cart'] = []
    store_items = Product.objects.all()
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'store_items':store_items, 'cart':cart, 'cart_size':len(cart)}
    main_page = render(request, 'catalog.html', ctx)

    if request.method == 'POST':
        cart.append(int(request.POST['obj_id']))
        return redirect("catalog")
    return main_page


def cart(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart)}
    return render(request, "cart.html", ctx)

def checkout(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart)}
    return render(request, "checkout.html", ctx)

def completeOrder(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart)}
    order = Order()
    order.items = genItemsList(cart)
    order.first_name = request.POST['first_name']
    order.last_name = request.POST['last_name']
    order.address = request.POST['address']
    order.city = request.POST['city']
    order.payment_data = request.POST['payment_data']
    order.fullfilled = False
    order.payment_method = request.POST['payment']
    order.save()
    request.session['cart'] = []
    return render(request, "complete_order.html", ctx)

def adminLogin(request):
    if request.method == "POST":
        usname = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(username=usname, password=pwd)
        if user is not None:
                login(request, user)
                return redirect("admin")
        else:
            return render(request, "admin_login.html", {'login': False})


    return render(request, "admin_login.html",None)


def adminDashboard(request):
    orders = Order.objects.all()
    ctx = {'orders': orders}
    return render(request, "admin_panel.html", ctx)

