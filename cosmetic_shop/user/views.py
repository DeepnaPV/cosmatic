from django.shortcuts import render,redirect
from inventory.models import products

# Create your views here.


def main(request):
    return render(request,'uhome.html')

def filter_products(request):
    category = request.GET.get('category', None)
    if category:
        filtered_products = products.objects.filter(category=category)
    else:
        filtered_products = products.objects.all()  

    return render(request, 'filter_products.html', {'products': filtered_products})

def detail(request, id):
    try:
        product = products.objects.get(id=id)
    except products.DoesNotExist:
        return redirect('allpro')  # Redirect to all products if the product is not found

    return render(request, 'uprodetail.html', {'product': product})