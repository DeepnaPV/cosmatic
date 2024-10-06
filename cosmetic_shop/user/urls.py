from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('uhome',views.main, name='main'),
    path('filter/', views.filter_products, name='filter_products'),
    path('product/<int:id>/', views.detail, name='product_detail'),

]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)