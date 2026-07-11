from .models import Cart
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, OrderItem


# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# Product Details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# Add To Cart
def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/admin/login/')

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')


# Cart
def cart(request):

    if not request.user.is_authenticated:
        return redirect('/admin/login/')

    items = Cart.objects.filter(user=request.user)

    grand_total = 0

    for item in items:
        item.total = item.product.price * item.quantity
        grand_total += item.total

    return render(request, 'cart.html', {
        'items': items,
        'total': grand_total
    })


# Increase Quantity
def increase_quantity(request, item_id):

    item = get_object_or_404(Cart, id=item_id)

    item.quantity += 1
    item.save()

    return redirect('cart')


# Decrease Quantity
def decrease_quantity(request, item_id):

    item = get_object_or_404(Cart, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# Remove Item
def remove_from_cart(request, item_id):

    item = get_object_or_404(Cart, id=item_id)
    item.delete()

    return redirect('cart')


# Checkout
def checkout(request):

    if not request.user.is_authenticated:
        return redirect('/admin/login/')

    items = Cart.objects.filter(user=request.user)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            total_price=total
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })


# Order Success
def order_success(request):
    return render(request, 'order_success.html')
# Register
def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# Login
def user_login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Logout
def user_logout(request):
    logout(request)
    return redirect('home')
from .models import Order

def my_orders(request):

    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })