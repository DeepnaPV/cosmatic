from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import products
from .models import CartItem 
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, CustomerForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            login(request, user)
            return redirect('main')  
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()

    return render(request, 'uregister.html', {'user_form': user_form, 'customer_form': customer_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')  
        else:
            # Return an 'invalid login' error message.
            ...

    return render(request, 'ulogin.html')

def about(request):
    return render(request,'about.html')

def main(request):
    return render(request,'uhome.html')

from django.shortcuts import render
from inventory.models import products

def filter_products(request):
    # Get all unique categories for the dropdown
    categories = products.objects.values_list('category', flat=True).distinct()
    
    # Get category from URL parameter
    category = request.GET.get('category', None)

    # Get price range from URL parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Start with all products
    filtered_products = products.objects.all()

    # Filter products based on category
    if category and category != 'all':
        filtered_products = filtered_products.filter(category=category)

    # Filter products based on price range
    if min_price:
        filtered_products = filtered_products.filter(price__gte=min_price)
    if max_price:
        filtered_products = filtered_products.filter(price__lte=max_price)

    context = {
        'products': filtered_products,
        'categories': categories,
        'current_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }
    
    return render(request, 'filter_products.html', context)


def detail(request, id):
    try:
        product = products.objects.get(id=id)
    except products.DoesNotExist:
        return redirect('allpro')  # Redirect to all products if the product is not found

    return render(request, 'uprodetail.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(products, id=product_id)
    return render(request, 'uprodetail.html', {'product': product})

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(products, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart.")
    else:
        messages.warning(request, "You need to be logged in to add items to your cart.")
    
    return redirect('filter_products')  # Redirect to the products page or wherever you prefer

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        messages.warning(request, "You need to be logged in to view your cart.")
        return redirect('ulogin')

def update_cart(request, product_id):
    item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increment':
            item.quantity += 1
            item.save()
        elif action == 'decrement':
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                # Optionally, remove the item if quantity reaches zero
                item.delete()
    
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
    item.delete()
    return redirect('view_cart')  # Redirect to the cart page


def checkout_view(request, product_id):
    # Retrieve the product using the provided product_id
    product = get_object_or_404(products, id=product_id)
    
    # Check if the request method is POST for handling form submission
    if request.method == 'POST':
        # Handle payment processing here
        # You can integrate with a payment gateway API
        # For now, we will just simulate a successful payment

        # After payment processing
        # Redirect to a success page or render a success template
        return render(request, 'payment_success.html', {'product': product})

    # If GET request, render the checkout page with the product details
    return render(request, 'check_out.html', {'product': product})
