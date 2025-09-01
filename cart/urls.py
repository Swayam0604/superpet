from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add-to-cart/<int:productId>',views.add_to_cart,name='add-to-cart'),
    path('delete-cart-item/<int:cartitem_id>',views.delete_cart_item,name="delete-cart-item"),
    path('update-cart-item/<int:cartitem_id>',views.update_cart_item,name='update-cart-item'),
    path('checkout/',views.checkout,name="checkout"),
    path('payment/<str:order_id>',views.payment,name="payment"),
    path('payment/payment-success/<str:order_id>',views.payment_success,name="payment-success"),
    path('order',views.order,name='order')
]
