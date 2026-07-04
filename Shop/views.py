from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Order


def home(request):
    return render(request, 'index.html')


def shop(request):
    try:
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})
    except Exception as e:
        messages.error(request, f"Error loading products: {e}")
        return render(request, 'shop.html')


def contact(request):
    return render(request, 'contact.html')


def why(request):
    return render(request, 'why.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")

                if user.is_superuser:
                    return redirect('/admin/')
                return redirect('home')

            messages.error(request, "Invalid username or password.")

        except Exception as e:
            messages.error(request, f"Login error: {e}")

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


@login_required
def add_to_cart(request, id):
    try:
        product = get_object_or_404(Product, id=id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, "Product added to cart successfully!")

    except Exception as e:
        messages.error(request, f"Unable to add product: {e}")

    return redirect('cart')


@login_required
def cart_view(request):
    try:
        items = Cart.objects.filter(user=request.user)

        total = sum(
            item.product.price * item.quantity
            for item in items
        )

        return render(request, 'cart.html', {
            'items': items,
            'total': total
        })

    except Exception as e:
        messages.error(request, f"Error loading cart: {e}")
        return redirect('shop')


@login_required
def place_order(request):
    try:
        items = Cart.objects.filter(user=request.user)

        if not items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart')

        for item in items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_amount=item.product.price * item.quantity
            )

        items.delete()
        messages.success(request, "Order placed successfully!")

    except Exception as e:
        messages.error(request, f"Order failed: {e}")

    return redirect('orders')


@login_required
def orders(request):
    try:
        user_orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', {
            'orders': user_orders
        })

    except Exception as e:
        messages.error(request, f"Error loading orders: {e}")
        return redirect('home')


@login_required
def remove_from_cart(request, id):
    try:
        item = get_object_or_404(
            Cart,
            id=id,
            user=request.user
        )
        item.delete()
        messages.success(request, "Item removed from cart.")

    except Exception as e:
        messages.error(request, f"Unable to remove item: {e}")

    return redirect('cart')