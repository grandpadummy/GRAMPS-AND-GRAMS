
from django.db import models
from django.contrib.auth.models import User
from app.models import Product, Profile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    shipping_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, null=True, blank=True)
    shipping_zip_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=100)
    shipping_phone_number = models.CharField(max_length=20)

    # Dont pluralize the table name
    class Meta:
        verbose_name_plural = "Shipping Address"

        def __str__(self):
            return f"Shipping Address - {str(self.id)}"
        

            


        
        # Create user shipping by default   

def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        user_shipping_address = ShippingAddress(shipping_user=instance)
        user_shipping_address.save()
post_save.connect(create_shipping_address, sender=User) 






class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    shipping_address1 = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Order - {str(self.id)}"
    

# Auto add shipping date

@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item - {str(self.id)}"






# def __str__(self):
#          return self.user.username
    
#         def __str__(self):
#                 return self.user.username





# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     shipping_address = models.TextField(max_length=15000)
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     date_ordered = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return f"Order - {str(self.id)}"
    

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order Item - {str(self.id)}"