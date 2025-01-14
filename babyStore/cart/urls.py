from django.urls import path, include
from .views import CartView,QuantityUpdateView


urlpatterns = [
    path('list/',CartView.as_view(),name='cart'),
    path('quantity/',QuantityUpdateView.as_view())
]