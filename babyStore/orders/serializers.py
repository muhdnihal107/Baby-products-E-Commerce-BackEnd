from rest_framework import serializers
from .models import Order
from cart.serializers import CartSerializer,CartItemsSerializer

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) 
    # StringRelatedField: This field displays a string representation of the related object 
    # (in this case, the user). It's useful when you don't need to display the entire object, 
    # but just a basic representation. For example, if you want to show the user's username, email,
    # or any other field defined in the __str__ method of the User model (or a related field like
    # username), StringRelatedField will automatically use the string representation of the related User model.
    cart = CartSerializer(read_only=True)
    cart_items = serializers.SerializerMethodField()  # To include details of cart items
    total_amount = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    class Meta:
        model = Order
        fields = [
            'id','user','cart','cart_items','payment_method','payment_status','payment_amount','total_amount',
            'status','address','created_at','updated_at','first_name','last_name','phone_number',
            'email','state','pincode'
        ]
        
    def get_cart_items(self, obj):
        """
        Serialize the cart items related to this order.
        """
        cart_items = obj.cart_items.all()  # Access related CartItems
        return CartItemsSerializer(cart_items, many=True).data
    