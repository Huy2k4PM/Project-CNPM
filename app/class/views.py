from django.views import View
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
from .models import User  # Import model User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import *
from django.utils import timezone
from django.db import transaction

def signup_views(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            messages.info(request, 'Passwords do not match!!!')
            return redirect('signup')
        else:
            myuser = User.objects.create_user(username=uname, email=email, password=pass1)  # Sử dụng create_user từ model User
            myuser.save()
            messages.success(request, "Registered successfully Log in now.")
            return redirect('login')

    return render(request, 'signup.html')

def login_views(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        print(username,pass1)
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            request.session['logged_in'] = True  # Đặt biến session 'logged_in' là True
            return redirect('product_list')
        else: messages.info(request,'User or password not correct!')
    return render(request,'login.html')

def logout_views(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']  # Xóa biến session nếu tồn tại
    logout(request)
    return redirect('product_list')

def search_views(request):
    searched = None
    keys= []
    if request.method == 'POST':
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    return render(request, 'search.html',{"searched":searched,"keys":keys})


def home_views(request):
    return render(request,'home.html')

# class LoginClass(View):

#     def get(self,request):
#         return render(request,'login.html')

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)  # Use the user object here
#             return redirect('home')  # Redirect to the home page or any other page after successful login
#         else:
#             return redirect('login')  # Redirect back to the login page if authentication fails


# def home(request):
#     products = Product.objects.all()
#     context = {'products':products}
#     return render(request,'app/home.html',context)

@login_required
def product_views(request):
    p = Product.objects.all()
    return render (request,'product.html',{'product':p})

def product_list(request):
    products = Product.objects.all()  # Query all products
    return render(request, 'home.html', {'products': products})


def shopping_cart_views(request):
    cart = ShoppingCart.objects.all()
    return render (request,'shopping_cart.html',{'shopping_cart':cart})

@login_required
def get_user_cart(request):
    user = request.user
    user_cart = ShoppingCart.objects.filter(user=user)
    return render(request, 'shopping_cart.html', {'cart': user_cart})

#xoa san pham
@login_required
def remove_from_cart(request, item_id):
    item = ShoppingCart.objects.get(id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.total_price = item.product.price * item.quantity
        item.save()
    else:
        item.delete()
    return redirect('get_user_cart')


#them san pham
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart.quantity += 1
    cart.save()
    return redirect('get_user_cart')

#xem chi tiet san pham
def product_detail(request):
    item = Product.objects.all()
    return render(request,'index.html',{'item':item})

@login_required
def process_payment(request):
    user = request.user
    user_cart = ShoppingCart.objects.filter(user=user)
    total = sum(item.total_price for item in user_cart)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = user
            payment.total_price = total
            payment.date = timezone.now()
            # Assuming one shopping cart per user for simplicity
            payment.shopping_cart = user_cart.first() if user_cart else None
            payment.transaction_of_customer = generate_transaction_id()  # Replace with your logic
            payment.transaction_of_merchant = generate_transaction_id()  # Replace with your logic
            payment.save()
            return redirect('OrderDetail')  # Replace with your success URL
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'cart': user_cart, 'total': total, 'form': form})

def generate_transaction_id():
    # Implement your logic for generating unique transaction IDs
    return random.randint(100000, 999999)

def payment_success(request):
    item = ShoppingCart.objects.all()
    item.delete()
    return render(request, 'payment.html')


def FeedBack_form(request):
    return render(request,'feedback.html')

def feedback(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Kiểm tra xem người dùng đã đăng nhập hay chưa
            user = request.user
            feedback_text = request.POST.get('feedback')
            feedback_obj = FeedBack.objects.create(user=user, feedback=feedback_text)
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('product_list')
        else:
            messages.error(request, 'Please login to submit feedback.')  # Thông báo lỗi nếu người dùng chưa đăng nhập
            return redirect('login')  # Chuyển hướng đến trang đăng nhập

    return render(request, 'feedback.html')

@login_required
def Order_view(request):
    user = request.user
    user_cart = ShoppingCart.objects.filter(user=user)
    
    if not user_cart.exists():
        return render(request, 'OrderDetail.html', {'cart': [], 'total': 0, 'message': "Your cart is empty."})
    
    total = sum(item.total_price for item in user_cart)

    order_details = []

    try:
        with transaction.atomic():
            for item in user_cart:
                order_detail = OrderDetail.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price,
                    date=timezone.now()  # Set the current time as the order date
                )
                order_details.append(order_detail)
            # Now delete the items from the cart
            user_cart.delete()
        
        message = "Your order has been placed successfully!"
    except Exception as e:
        message = f"An error occurred while placing your order: {str(e)}"
        order_details = []  # Clear order details in case of error

    return render(request, 'OrderDetail.html', {'cart': order_details, 'total': total, 'message': message})

def text(request):
    return render(request,'index.html')

@login_required
def History_order(request):
    user=request.user
    items = OrderDetail.objects.filter(user=user)
    return render(request,'history_order.html',{'cart':items})