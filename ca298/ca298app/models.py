from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser


class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    picture = models.FileField(upload_to='category_img/', blank=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.FileField(upload_to='product_img/', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10000, decimal_places=1)
    dimensions = models.CharField(max_length=400)


class CaUser(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CaUser, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    shipping_address = models.CharField(max_length=500)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.DecimalField(max_digits=19, decimal_places=0)
    cvv_number = models.DecimalField(max_digits=3, decimal_places=0)


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def price(self):
        return self.product.price * self.quantity


class ShoppingBasket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CaUser, on_delete=models.CASCADE)


class ShoppingBasketItems(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)



