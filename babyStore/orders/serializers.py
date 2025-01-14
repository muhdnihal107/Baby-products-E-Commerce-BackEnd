from rest_framework import serializers
from .models import Order
from cart.serializers import CartSerializer

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) 
    # StringRelatedField: This field displays a string representation of the related object 
    # (in this case, the user). It's useful when you don't need to display the entire object, 
    # but just a basic representation. For example, if you want to show the user's username, email,
    # or any other field defined in the __str__ method of the User model (or a related field like
    # username), StringRelatedField will automatically use the string representation of the related User model.
    cart = CartSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    status = serializers.ChoiceField(choices=Order.ORDER_STATUS_CHOICES)
    class Meta:
        model = Order
        fields = [
            'id','user','cart','payment_method','payment_status','payment_amount','total_amount',
            'status','address','created_at','updated_at'
        ]
    