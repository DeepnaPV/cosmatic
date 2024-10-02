from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import creatproduct
from .models import products,inventordetails
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import createuser,createinventor
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import views as auth_views

# Create your views here.


def main(request):
    return render(request,'home.html')

def registerpage(request):
    if request.method == 'POST':
        form = createuser(request.POST)
        if form.is_valid():
            form.save()  # Saving the form data to the database
            return HttpResponse('User successfully registered')
    else:
        form = createuser()
    return render(request, 'register.html', {'form': form})

def loginpage(request):
    if request.method == 'POST':
        usernam = request.POST['usern']
        passwor = request.POST['passw']
        if not usernam or not passwor:
            messages.error(request, 'Both fields are required.')
            return render(request, 'login.html')
        user = authenticate(request, username=usernam, password=passwor)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in.')
            return redirect('main')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect(loginpage)


def addpro(request):
    if request.method == 'POST':
        form=creatproduct(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else: 
        form=creatproduct()
    return render(request,'addprod.html',{'form':form})

def updatepro(request,id):
    pro=products.objects.get(id=id)
    if request.method == 'POST':
        form=creatproduct(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
    else:
        form=creatproduct(instance=pro)
    return render(request,'addprod.html',{'form':form})

def deletepro(request,id):
    pro=products.objects.get(id=id)
    if request.method == 'POST':
        pro.delete()
        return redirect(addpro)
    return render (request,'deletepro.html',{'pro':pro})

def viewpro(request):
    pro=products.objects.all()
    return render(request,'viewpro.html',{'form':pro})


def allprod(request):
    c1=products.objects.all()
    return render(request,'allpro.html',{'c1':c1})


def purchase_product(request, id):
    product = get_object_or_404(products, id=id)
    if product.stock > 0:
        product.stock -= 1
        product.save()
        if product.stock == 1:
            check_stock_and_alert(product)
        return redirect('view_product', id=product.id)  # Changed to 'view_product'
    else:
        return HttpResponse("Product is out of stock")
    


def check_stock_and_alert(product):
    if product.stock == 1:
        recipient_list = User.objects.values_list('email', flat=True)
        
        subject = f"Low Stock Alert: {product.name}"
        message = f"The stock for {product.name} has reached 1. Please restock soon."
        
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
        print(f"Low stock alert for {product.name} sent successfully")
    else:
        print(f"Stock level for {product.name} is {product.stock}, no alert needed.")

def user_details(request, id=None):
    usr = None  # To store inventordetails instance
    user_data = None  # To store user (email, username) information
    
    if id:
        try:
            usr = inventordetails.objects.get(id=id)  # Retrieve inventor details
            user_data = usr.user  # Assuming inventordetails has a ForeignKey to User model
        except inventordetails.DoesNotExist:
            usr = None
        except User.DoesNotExist:
            user_data = None

    if request.method == 'POST':
        form = createinventor(request.POST, request.FILES, instance=usr)
        if form.is_valid():
            form.save()
    else:
        form = createinventor(instance=usr)

    # Prepare context including both inventor and user data
    context = {
        'form': form,
        'user': usr,  # The inventor details
        'username': user_data.username if user_data else None,  # Fetch username
        'email': user_data.email if user_data else None  # Fetch email
    }
    
    return render(request, 'view_user.html', context)


def product_detail(request, id):
    try:
        product = products.objects.get(id=id)
    except products.DoesNotExist:
        return redirect('allpro')  # Redirect to all products if the product is not found

    return render(request, 'product_detail.html', {'product': product})
