from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from apps import views
from apps.views import (
    index, shop, detail, Cart, register, user_login, user_logout, help, update_cart_quantity,
    remove_from_cart, add_to_cart, add_to_like, LikeView, remove_from_like, profile, about, checkout, edit_profile
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('shop/', shop, name='shop'),   
    path('detail/<int:pk>/', detail, name='detail'),
    path('profile/', profile, name='profile'),
    path('cart/', Cart.as_view(), name='cart'),
    path('like/', LikeView.as_view(), name='like'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logaut/', user_logout, name='logaut'),

    path('accounts/', include('allauth.urls')),

    path('help/', help, name='help'),
    path('about/', about, name='about'),

    path('update-quantity/', update_cart_quantity, name='update_quantity'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('add-to-like/', add_to_like, name='add_to_like'),
    path('remove-from-like/<int:pk>/', remove_from_like, name='remove_from_like'),

    path('checkout/', checkout, name='checkout'),

    path('profile-edit/', views.edit_profile, name='edit_profile'),


]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

