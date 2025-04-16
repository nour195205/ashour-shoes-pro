from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('products/<int:product_id>/', views.product_details, name='product_details'),
    path('filter/', views.filter_products, name='filter_products'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('contactus/', views.contact_us, name='contact_us'),
    path('orders/', views.view_orders, name='orders'),
    path('custom-order/', views.custom_order, name='custom_order'),
    path('submit-custom-order/', views.submit_custom_order, name='submit_custom_order'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),  # جديد
    path('paymob/callback/', views.paymob_callback, name='paymob_callback'),  # جديد
]