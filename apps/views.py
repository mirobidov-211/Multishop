# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from httpx import post, get, request
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.views.generic import ListView
from django.contrib import messages
from .models import Category, Product, User, Comment, Color, Size, Wishlist, Like, Product2

TELEGRAM_BOT_TOKEN = '8024211878:AAHdSAoVZwPr9MK2PU_OCwczWd6FcqjcF48'


def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = get(url, params=params)
    print(response.text, response.status_code)



TELEGRAM_BOT_TOKEN1 = '7452966493:AAHz87E7RucEAHzSErOBK33tx2POhNwIAZ4'


def send_message(chat_id, message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN1}/sendMessage'
    params1 = {
        'chat_id': chat_id,
        'text': message
    }
    response1 = get(url, params=params1)
    print(response1.text, response1.status_code)



def index(request):
    category = Category.objects.all()
    category_id = request.GET.get('category_id')
    q = request.GET.get('q')

    products = Product.objects.all()
    if q:
        products = products.filter(name__icontains=q)
    if category_id:
        products = products.filter(category_id=category_id)

    newest_products = Product.objects.order_by('-created_at')

    product2 = Product2.objects.filter(is_active=True)

    context = {
        'products': products,
        'products2': newest_products,
        'category': category,
        'product2': product2
    }
    return render(request, 'product/index.html', context)


def shop(request):
    category = Category.objects.all()
    color_ids = request.GET.getlist('color')
    size_ids = request.GET.getlist('size')
    price_range = request.GET.get('price')
    category_id = request.GET.get('category_id')
    q = request.GET.get('q')

    products = Product.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()

    if color_ids:
        products = products.filter(colors__id__in=color_ids).distinct()
    if size_ids:
        products = products.filter(size__id__in=size_ids).distinct()
    if price_range:
        try:
            price_min, price_max = map(int, price_range.split('-'))
            products = products.filter(price__gte=price_min, price__lte=price_max)
        except:
            pass
    if q:
        products = products.filter(name__icontains=q)
    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'category': category,
        'colors': colors,
        'sizes1': sizes,
        'selected_colors': color_ids,
        'selected_sizes': size_ids,
        'selected_price': price_range,
        'price_ranges': [
            ('0-100', '$0 - $100'),
            ('100-200', '$100 - $200'),
            ('200-300', '$200 - $300'),
            ('300-500', '$300 - $500'),
        ]
    }
    return render(request, 'product/shop.html', context)


def detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('text1')
        text = request.POST.get('text')

        Comment.objects.create(
            email=email,
            name=name,
            text=text,
            product=product
        )
        return redirect(f'/detail/{pk}')

    comment_list = product.comments.all()
    context = {
        'product': product,
        'comment_list': comment_list
    }
    return render(request, 'product/detail.html', context)


def profile(request):

    return render(request, 'product/profile.html',)


def register(request):
    if request.method == 'POST':
        ism = request.POST.get('ism')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=ism).exists():
            messages.error(request, "Bu username allaqachon mavjud. Boshqasini tanlang.")
            return redirect('/register/')

        User.objects.create(
            username=ism,
            email=email,
            password=make_password(password)
        )

        user = authenticate(username=ism, password=password)
        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'user/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")

    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def help(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        text = f"Yordam so'rovi:\n\nIsm: {name}\nEmail: {email}\nXabar: {message}"
        send_message(7576554067, text)


    return render(request, 'product/help.html')


def about(request):

    return render(request, 'product/about.html')


class Cart(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'product/cart.html'
    context_object_name = 'my_products'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset().filter(user=user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_products = context['my_products']
        total_price = sum([item.total_price for item in my_products])
        context['total_price'] = total_price
        return context


@require_POST
@login_required
def checkout(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    
    if not wishlist_items.exists():
        messages.error(request, "Savat bo‘sh!")
        return redirect('cart')

    total_price = sum([item.total_price for item in wishlist_items])
    
    # Xabarni tayyorlash
    message = f"🛒 *Yangi buyurtma!*\n👤 Foydalanuvchi: {user.username}\n\n"
    for item in wishlist_items:
        message += f"📦 {item.product.name} — {item.quantity} dona — ${item.total_price:.2f}\n"
    message += f"\n💰 Umumiy narx: ${total_price:.2f}"

    # Telegram guruhga yuborish (guruh chat_id'sini alohida tekshiring)
    send_message(chat_id='-1002773306988', message=message)

    messages.success(request, "Buyurtma qabul qilindi!")
    return redirect('cart')

    


@csrf_exempt
@require_POST
@login_required
def update_cart_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    action = data.get('action')

    wishlist_item = Wishlist.objects.filter(user=request.user, product_id=product_id).first()

    if not wishlist_item:
        return JsonResponse({'error': 'Mahsulot topilmadi'}, status=404)

    if action == 'plus':
        wishlist_item.quantity += 1
    elif action == 'minus' and wishlist_item.quantity > 1:
        wishlist_item.quantity -= 1

    wishlist_item.save()

    # Umumiy savat narxini qayta hisoblash
    all_items = Wishlist.objects.filter(user=request.user)
    total = sum([item.total_price for item in all_items])

    return JsonResponse({
        'quantity': wishlist_item.quantity,
        'total_price': wishlist_item.total_price,
        'cart_total': total
    })



@require_POST
@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        wishlist_item.quantity += 1
        wishlist_item.save()

    return redirect('cart')



@csrf_exempt
@require_POST
@login_required
def remove_from_cart(request):
    import json
    data = json.loads(request.body)
    product_id = data.get('product_id')

    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'success': True})

class LikeView(LoginRequiredMixin, ListView):
    model = Like
    template_name = 'product/like.html'
    context_object_name = 'my_like'
    login_url = 'login'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)


@login_required
def add_to_like(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        like_item, created = Like.objects.get_or_create(user=request.user, product=product)

        if not created:
            like_item.quantity += 1
        like_item.save()
    return redirect('like')



@csrf_exempt
@require_POST
@login_required
def remove_from_like(request):
    import json
    data = json.loads(request.body)
    product_id = data.get('product_id')

    Like.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'success': True})



def remove_from_like(request, pk):
    if request.user.is_authenticated:
        like = get_object_or_404(Like, user=request.user, product_id=pk)
        like.delete()
    return redirect('like')  # like sahifasiga qaytaradi



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if request.FILES.get('image'):
            user.image = request.FILES['image']

        user.save()
        return redirect('profile')  # profil sahifasiga qaytadi

    return render(request, 'product/edit_profile.html')