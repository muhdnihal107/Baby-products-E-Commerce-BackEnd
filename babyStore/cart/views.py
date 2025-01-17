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
        cart,created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
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
    def get(self,request,pk):
        cart = get_object_or_404(Cart,pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk):
        action = request.data.get('action')
        product_id = request.data.get('product_id')
        
        if not action or not product_id:
            return Response({"errors:action or productid is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
       # cart = get_object_or_404(Cart,user=request.user)
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        cartitem = get_object_or_404(CartItems,cart_id = pk,product_id=product_id)
        
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
        
class RemoveProductCart(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,cart_id,product_id):
        try:
            cart = get_object_or_404(Cart,id=cart_id,user=request.user)
            cart_item = get_object_or_404(CartItems, cart=cart,product_id=product_id)
            cart_item.delete()
            return Response({"message": "Product removed from the cart successfully."},status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except CartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart."}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
        
        
        
        
        
        
        

