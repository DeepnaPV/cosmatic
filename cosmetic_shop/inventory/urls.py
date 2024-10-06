from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import  include
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('home',views.main, name='main'),
    path('addpro',views.addpro,name='addpro'),
    path('update/<int:id>',views.updatepro,name='updatepro'),
    path('deletepro/<int:id>',views.deletepro,name='delpro'),
    path('viewpro',views.viewpro,name='allprot'),
    path('allpro',views.allprod,name='allpro'),
    path('register',views.registerpage,name='register'),
    path('login',views.loginpage,name='login'),
    path('viewuser/<int:id>',views.user_details,name='viewusr'),
    path('purchase/<int:id>/', views.purchase_product, name='purchase_product'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logout',views.logoutpage,name='logout'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),


]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)