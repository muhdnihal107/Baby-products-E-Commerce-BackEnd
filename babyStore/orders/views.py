from django.shortcuts import render
from rest_framework.views import APIView
from .models import Order,OrderItems
from .serializers import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from cart.models import Cart,CartItems

# Create your views here.

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,*args,**kwargs):
        user = request.user
        data = request.data

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "No active cart found for the user."}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = CartItems.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error":"the cart is empty."},status=status.HTTP_404_NOT_FOUND)
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number =data.get('phone_number')
        email = data.get('email')
        state = data.get('state')
        pincode = data.get('pincode')
        address = data.get('address')
        payment_method = data.get('payment_method')
        payment_amount = data.get('payment_amount')

        if not address or not payment_method:
            return Response({"error": "Address and payment method are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not payment_amount or float(payment_amount) <= 0:
            return Response({"error": "A valid payment amount is required."}, status=status.HTTP_400_BAD_REQUEST)
        
    

        order = Order.objects.create(
            user=user,
            cart=cart,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            state=state,
            pincode=pincode,
            address=address,
            payment_method=payment_method,
            payment_amount=payment_amount
        )
        
        order_items = [
            OrderItems(order=order, product=item.product, quantity=item.quantity)
            for item in cart_items
        ]
        OrderItems.objects.bulk_create(order_items)
        
        cart_items.delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

        # return Response({
        #     "message": "Order created successfully.",
        #     "order_id": order.id,
        #     "cart":cart.id,
        #     "status": order.status,
        #     "first_name":order.first_name,
        #     "last_name":order.last_name,
        #     "phone_number":order.phone_number,
        #     "email":order.email,
        #     "state":order.state,
        #     "pincode":order.pincode,
        #     "address":order.address,
        #     "payment_status": order.payment_status,
        #     "created_at": order.created_at
        # }, status=status.HTTP_201_CREATED)
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user
        try:
            last_order = Order.objects.filter(user=user).order_by('-created_at').first()
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or you do not have permission to view this order."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(last_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    
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


