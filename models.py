# from django.db import models
# from django.contrib.auth.models import User
# import store.models



# # Model Khách hàng
# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name if self.name else "Khách hàng chưa đặt tên"


# # Model Sản phẩm
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  
#     stock = models.IntegerField(default=0)
#     digital = models.BooleanField(default=False, null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)

#     def __str__(self):
#         return self.name

#     # @property
#     # def price_vnd(self):
#     #     """Chuyển đổi giá từ USD sang VND khi hiển thị"""
#     #     exchange_rate = 24000 
#     #     return self.price * exchange_rate

#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url

# # Model Đơn hàng
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)

#     def __str__(self):
#         return f"Đơn hàng {self.id}"

#     @property
#     def shipping(self):
#         """Kiểm tra xem đơn hàng có cần giao hàng không"""
#         return any(not item.product.digital for item in self.orderitem_set.all() if item.product)

#     @property
#     def get_cart_total(self):
#         return sum(item.get_total for item in self.orderitem_set.all())

#     @property
#     def get_cart_items(self):
#         return sum(item.quantity for item in self.orderitem_set.all())

# # Model Sản phẩm trong đơn hàng
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, default=49)  # Không để null để tránh mất dữ liệu
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.name if self.product else 'Không có sản phẩm'} - {self.quantity} sản phẩm"

#     @property
#     def get_total(self):
#         return self.product.price * self.quantity if self.product else 0

# # Model Giỏ hàng
# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
#     quantity = models.IntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product.name} ({self.quantity})"

#     @property
#     def get_total(self):
#         return self.product.price * self.quantity if self.product else 0

# class OrderHistory(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_id = models.CharField(max_length=200, null=True)
#     created_at = models.DateTimeField()
#     deleted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Lịch sử đơn hàng {self.transaction_id}"

# # Model Địa chỉ giao hàng
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Ràng buộc để tránh lỗi dữ liệu
#     address = models.CharField(max_length=255, default="Chưa có địa chỉ")
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zipcode = models.CharField(max_length=20)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.address}, {self.city}"
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


# 🔹 Model Khách hàng
class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Sử dụng settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, default='Khách hàng')
    email = models.EmailField()


# 🔹 Model Sản phẩm
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.IntegerField(default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        return self.image.url if self.image else ''


# 🔹 Model Đơn hàng
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Đơn hàng {self.id}"

    @property
    def shipping(self):
        return any(not item.product.digital for item in self.orderitem_set.all() if item.product)

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())


# 🔹 Model Sản phẩm trong đơn hàng
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name if self.product else 'Không có sản phẩm'} - {self.quantity} sản phẩm"

    @property
    def get_total(self):
        return self.product.price * self.quantity if self.product else 0
class OrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lịch sử đơn hàng {self.transaction_id}"


# 🔹 Model Địa chỉ giao hàng
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    address = models.CharField(max_length=255, default="Chưa có địa chỉ")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}, {self.city}"
