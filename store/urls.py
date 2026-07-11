from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('my-orders/', views.my_orders, name='my_orders'),

    path('', views.home, name='home'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),

    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),

    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('order-success/', views.order_success, name='order_success'),

]