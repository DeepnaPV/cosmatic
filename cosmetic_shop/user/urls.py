from django.urls import path
from . import views

urlpatterns=[
    path('uhome',views.main, name='main'),
]