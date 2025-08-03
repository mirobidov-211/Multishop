from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    # name = models.CharField(max_length=255)
    hex_code = models.CharField(max_length=30)

    def __str__(self):
        return self.hex_code

    
class Size(models.Model):
    # name = models.CharField(max_length=255)
    size = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.size
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    sale = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    count = models.IntegerField(default=0)
    about = models.TextField()
    information = models.JSONField(default=dict)
    about2 = models.TextField()
    colors = models.ManyToManyField(Color, related_name='colors')
    size = models.ManyToManyField(Size, related_name='sizees', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name

    @property
    def sale_price(self):
        return self.price - (self.price * self.sale / 100)


class Product2(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = ResizedImageField(size=[900, 900], crop=['middle', 'center'], upload_to='mahsulotlar/')
    about = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = ResizedImageField(size=[900, 900], crop=['middle', 'center'], upload_to='mahsulotlar/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)
    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return self.username
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users2')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products2')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.sale_price
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='liked_products')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.sale_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"