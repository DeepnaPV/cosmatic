from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('register/',views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('about',views.about,name='about'),
    path('uhome',views.main, name='main'),
    path('contact',views.contact, name='contact'),
    path('filter/', views.filter_products, name='filter_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/<int:product_id>/', views.checkout_view, name='checkout'),
    path('logout',views.logoutpage,name='logout'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),


]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)