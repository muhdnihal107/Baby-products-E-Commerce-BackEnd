from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Cart,CartItems
from .serializers import CartItemsSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemsSerializer(data = request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            cart_item,created = CartItems.objects.get_or_create(cart=cart,product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()
            
            return Response(CartSerializer(cart).data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        cart = Cart.objects.filter(user = request.user).first()
        if cart:
            cart.items.all().delete()
        return Response({"message":"cart is cleared"},status=status.HTTP_204_NO_CONTENT)
class QuantityUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request):
        action = request.data.get('action')
        product_id = request.data.get('product_id')
        
        if not action or not product_id:
            return Response({"errors:action or productid is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
       # cart = get_object_or_404(Cart,user=request.user)
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        cartitem = get_object_or_404(CartItems,user=request.user,product_id=product_id)
        
        if action == "increment":
            cartitem.quantity += 1
        elif action == "decrement":
            if cartitem.quantity >= 1:
                cartitem.quantity -= 1
            else:
                cartitem.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cartitem.save()
        return Response({
            'message': 'Cart item updated successfully.',
            'product_id': product_id,
            'new_quantity': cartitem.quantity
        },status=status.HTTP_200_OK)
        
        
        
        
        
        
        
        
        

