from django.db import models
from django.conf import settings
from cart.models import Cart

# Create your models here.
class Order(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    cart = models.OneToOneField(Cart,on_delete=models.PROTECT,related_name='order')
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default=PENDING)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"
