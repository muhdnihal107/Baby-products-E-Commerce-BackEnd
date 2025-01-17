from django.urls import path, include
from .views import CartView,QuantityUpdateView,RemoveProductCart


urlpatterns = [
    path('list/',CartView.as_view(),name='cart'),
    path('quantity/<int:pk>',QuantityUpdateView.as_view()),
    path('remove/<int:cart_id>/<int:product_id>/', RemoveProductCart.as_view(), name='remove-product'),
]