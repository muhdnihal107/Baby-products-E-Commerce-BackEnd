from django.urls import path, include
from .views import OrderCreateView, OrderDetailView, OrderListView, OrderStatusUpdateView,OrderDlatailedView,razorpay_webhook


urlpatterns = [
    path('list/', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('detail/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('details/<int:pk>', OrderDlatailedView.as_view(), name='order-details'),
    path('razorpay-webhook/', razorpay_webhook, name='razorpay-webhook'),


]