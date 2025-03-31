from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('filter', views.filter_products, name='filter'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.view_orders, name='orders'),
    path('contactus/', views.contact_us, name='contact_us'),
]