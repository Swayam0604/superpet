from django.shortcuts import render
from product.models import Product,Category
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.

def products(request):
    products=Product.objects.all()
    start_price = request.GET.get("sp")
    end_price = request.GET.get("ep")

    brand = request.GET.get("brand")
    if brand:
        products = Product.objects.filter(product_brand__iexact=brand)
        return render(request,"products.html",{'products':products})

    if start_price and end_price:
        products=Product.objects.filter(product_price__gte=start_price,product_price__lte=end_price)
        return render(request,"products.html",{'products':products})

    return render(request,"products.html",{'products':products})

class ProductList(ListView):
    model=Product

class ProductDetail(DetailView):
    model=Product

        

class CategoryDetail(DetailView):
    model=Category
    template_name="category/category.html"
    context_object_name="category"
    slug_field="category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context["products"]=Product.objects.all()
        print(context)
        return context
       