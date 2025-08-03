from django.contrib import admin
from .models import Category, Product, ProductImage, User, Comment, Color, Size, Wishlist, Like, Product2

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id' )
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'category', 'price', 'sale', 'count')
    search_fields = ('name', 'category__name')
    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', )
    search_fields = ('product__name',)




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email',)
    search_fields = ('username', 'email',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email', 'product', 'created_at')
    search_fields = ('name', 'email', 'product__name')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('hex_code', 'id')
    search_fields = ('hex_code',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'id')
    search_fields = ('id', )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'id')
    search_fields = ('user__username', 'product__name')

@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = ('user', 'product', 'id')
    search_fields = ('user__username', 'product__name')



@admin.register(Product2)
class Product2Admin(admin.ModelAdmin):
    list_display = ('name', 'id', 'category', 'img')
    search_fields = ('name', 'category__name')