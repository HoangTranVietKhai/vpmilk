from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import json
import datetime
import traceback
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError 
from .forms import RegisterForm
from .utils import guestOrder
from .models import Customer, Product, Order, OrderHistory, OrderItem, ShippingAddress
from django.contrib import messages 
from django.contrib.auth.forms import UserCreationForm

# 🔹 Đăng ký tài khoản
# 🔹 Đăng ký tài khoản
from django.db import IntegrityError  # Thêm dòng import này

# 🔹 Đăng ký tài khoản
def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect("/")
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Kiểm tra email tồn tại
                    if User.objects.filter(email=form.cleaned_data['email'].lower()).exists():
                        form.add_error('email', 'Email này đã được đăng ký')
                        return render(request, "store/register.html", {"form": form})
                    
                    # Tạo user
                    user = form.save(commit=False)
                    user.email = form.cleaned_data['email'].lower()
                    user.username = form.cleaned_data['username'].lower()  # Chuẩn hóa username
                    user.save()
                    
                    # Tạo customer
                    customer, created = Customer.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': user.username,
                            'email': user.email
                        }
                    )
                    
                    if not created:
                        customer.name = user.username
                        customer.email = user.email
                        customer.save()
                    
                    login(request, user)
                    messages.success(request, "Đăng ký thành công!")
                    return redirect("/")
                    
            except IntegrityError as e:
                form.add_error(None, f"Lỗi tài khoản: {str(e)}")
            except Exception as e:
                form.add_error(None, f"Lỗi hệ thống: {str(e)}")
    else:
        form = RegisterForm()
    
    return render(request, "store/register.html", {"form": form})


# 🔹 Đăng nhập
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "store/login.html", {"form": form})


# 🔹 Đăng xuất
def logout_view(request):
    logout(request)
    return redirect("/login/")


# 🔹 Danh sách sản phẩm
def store(request):
    products = Product.objects.all()
    return render(request, 'store/store.html', {'products': products})


# 🔹 Chi tiết sản phẩm
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# 🔹 Giỏ hàng
def cart(request):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
    
    return render(request, "store/cart.html", {"items": items, "order": order})


# 🔹 Thanh toán
def checkout(request):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
    
    return render(request, "store/checkout.html", {"items": items, "order": order})


# 🔹 Cập nhật giỏ hàng
def updateItem(request):
    try:
        data = json.loads(request.body)
        productId = data.get('productId')
        action = data.get('action')

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Người dùng chưa đăng nhập'}, status=400)

        product = get_object_or_404(Product, id=productId)
        customer, _ = Customer.objects.get_or_create(user=request.user)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            if orderItem.quantity < product.stock:
                orderItem.quantity += 1
            else:
                return JsonResponse({'error': 'Không đủ hàng trong kho'}, status=400)
        elif action == 'remove':
            orderItem.quantity -= 1

        if orderItem.quantity <= 0:
            orderItem.delete()
        else:
            orderItem.save()

        return JsonResponse({'message': 'Cập nhật thành công', 'quantity': orderItem.quantity})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dữ liệu JSON không hợp lệ'}, status=400)
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'error': f'Lỗi server: {str(e)}'}, status=500)


# 🔹 Xử lý đơn hàng
def processOrder(request):
    if request.method != "POST":
        return JsonResponse({"error": "Phương thức không hợp lệ"}, status=400)

    try:
        data = json.loads(request.body)
        customer, order = guestOrder(request, data)

        if not order:
            return JsonResponse({'error': 'Không tìm thấy đơn hàng'}, status=400)

        order.complete = True
        order.transaction_id = data["transaction_id"]
        order.save()

        OrderHistory.objects.create(
            customer=order.customer,
            total_price=order.get_cart_total,
            transaction_id=data["transaction_id"],
            created_at=order.date_ordered
        )

        order.orderitem_set.all().delete()
        return JsonResponse({"message": "Đặt hàng thành công!", "order_id": order.id})

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({"error": f"Lỗi server: {str(e)}"}, status=500)
