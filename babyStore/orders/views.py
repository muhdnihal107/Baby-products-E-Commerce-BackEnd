from django.shortcuts import render
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart
# Create your views here.

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"error": "Cart does not exist for the user"}, status=status.HTTP_400_BAD_REQUEST)
        if hasattr(cart, 'order'):
            return Response({"error": "This cart has already been used to create an order."}, status=status.HTTP_400_BAD_REQUEST)
        if cart.items.count() == 0:
            return Response({"error": "Cart is empty. Cannot create an order."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(cart=cart,user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        order = get_object_or_404(Order,pk=pk,user = request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def delete(self,request,pk):
        order = get_object_or_404(Order,pk=pk,user = request.user)
        order.delete()
        return Response({"message": "Order deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if 'status' not in request.data:
            return Response({"error":"Status field is required"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = request.data['status']
        order.save()
        return Response({"message": "Order status updated successfully"}, status=status.HTTP_200_OK)  


