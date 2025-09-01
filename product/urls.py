from django.urls import path
from .import views
urlpatterns = [
    path('',views.products,name="product"),
    path('product-list',views.ProductList.as_view(),name="product-list"),
    path('product-details/<int:pk>',views.ProductDetail.as_view(),name="product-details"),
    path('<slug:slug>',views.CategoryDetail.as_view(),name='category-detail'),
    
]
