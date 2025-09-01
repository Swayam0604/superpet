from .models import Order, OrderItem
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields="__all__"
        exclude=["order_id","user","product","paid"]