from django.urls import path
from .views import login_view, register_view, logout_view
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .views import store
from .views import product_detail

urlpatterns = [
	#Leave as empty string for base url
	path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('product/<int:product_id>/', product_detail, name='product_detail'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)