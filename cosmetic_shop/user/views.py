from django.shortcuts import render,redirect,get_object_or_404
from inventory.models import products
from .models import CartItem 
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from .forms import UserRegistrationForm, CustomerForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


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
           error_message = "Invalid username or password."
           return render(request, 'ulogin.html', {'error': error_message})

    return render(request, 'ulogin.html')

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contactus.html')

def main(request):
    return render(request,'uhome.html')

from django.shortcuts import render
from inventory.models import products

def filter_products(request):
    categories = products.objects.values_list('category', flat=True).distinct()
    category = request.GET.get('category', None)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    filtered_products = products.objects.all()

    if category and category != 'all':
        filtered_products = filtered_products.filter(category=category)

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
        return redirect('allpro') 

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
    
    return redirect('filter_products')  

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        messages.warning(request, "You need to be logged in to view your cart.")
        return redirect('login')

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
                item.delete()
    
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
    item.delete()
    return redirect('view_cart') 

def checkout_view(request, product_id):
    product = get_object_or_404(products, id=product_id)
    
    if request.method == 'POST':
        return render(request, 'payment_success.html', {'product': product})

    return render(request, 'check_out.html', {'product': product})

def logoutpage(request):
    logout(request)
    return redirect('login')

def purchase_product(request, id):
    product = get_object_or_404(products, id=id)

    if request.method == 'POST':
        if product.stock > 0:
            product.stock -= 1
            product.save()

            if product.stock == 0:
                check_stock_and_alert(product)

            messages.success(request, f"You have successfully purchased {product.name}.")
            return redirect('product_details', id=product.id) 
        else:
            messages.error(request, "Sorry, this product is out of stock.")
            return redirect('product_details', id=product.id)

    return render(request, 'purchase_product.html', {'product': product})


def check_stock_and_alert(product):
    recipient_list = User.objects.values_list('email', flat=True)
    
    subject = f"Low Stock Alert: {product.name}"
    message = f"The stock for {product.name} has reached 0. Please restock soon."
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    print(f"Low stock alert for {product.name} sent successfully")

def payment_success(request, order_id):
    try:
        order = order.objects.get(id=order_id, user=request.user)
        context = {
            'order': order,
            'user': request.user,
        }
        return render(request, 'user/payment_success.html', context)
    except order.DoesNotExist:
        return redirect('shop')