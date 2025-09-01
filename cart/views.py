from django.shortcuts import render,HttpResponseRedirect
from .models import Cart,CartItem,Order,OrderItem
from product.models import Product
from .forms import OrderForm
from django.views.decorators.csrf import csrf_exempt
import uuid
import razorpay
from superpet import settings
from razorpay.errors import SignatureVerificationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login')
def cart(request):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    cartitems=cart.cartitem_set.all()
    total=0
    for cartitem in cartitems:
        total+=cartitem.quantity*cartitem.product.product_price
    return render(request,"cart.html",{"cartitems":cartitems,"total":total,"isEmpty":len(cartitems)==0})


@login_required(login_url='/login')
def add_to_cart(request,productId):
    current_user=request.user
    cart,created=Cart.objects.get_or_create(user=current_user)
    request.session['cart_id']=cart.id
    products=Product.objects.get(id=productId)
    cartitem,cartitem_created=CartItem.objects.get_or_create(cart=cart,product=products)

    quantity=int(request.GET.get('quantity'))
    if cartitem_created:
        cartitem.quantity=quantity  
    else:
        cartitem.quantity=cartitem.quantity+quantity

    cartitem.save()
    
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

@login_required(login_url='/login')
def delete_cart_item(request,cartitem_id):
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required(login_url='/login')
def update_cart_item(request,cartitem_id):
    cartitem=CartItem.objects.get(id=cartitem_id)
    quantity=request.GET.get('quantity')
    cartitem.quantity=quantity
    cartitem.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@login_required(login_url='/login') 
def checkout(request):
    if request.method=="GET":
        form=OrderForm()
        return render(request,"checkout.html",{"form":form})
    elif request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            order=Order.objects.create(
                order_id=str(uuid.uuid4())[:11],
                user=request.user,
                address_line_1=form.cleaned_data['address_line_1'],
                address_line_2=form.cleaned_data['address_line_2'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                pin_code=form.cleaned_data['pin_code'],
                phone_no=form.cleaned_data['phone_no'],
            )
            cart=Cart.objects.get(id=request.session.get('cart_id'))
            for cartitem in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=cartitem.product,
                    quantity=cartitem.quantity
                )
    return HttpResponseRedirect('/cart/payment/'+order.order_id)

@login_required(login_url='/login')
def payment(request,order_id):
    order=Order.objects.get(order_id=order_id)
    order_items=order.orderitem_set.all()

    total = 0
    for order_item in order_items:
        total += order_item.quantity * order_item.product.product_price

    client= razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRETS))
    data = { "amount": total*100, "currency": "INR", "receipt": order_id }
    payment_details = client.order.create(data=data)
    print(payment_details)
    return render(request,"payment.html",{"order":order,"order_items":order_items,"total":total,"razorpay_id":settings.RAZORPAY_ID,"payment_details":payment_details})

@login_required(login_url='/login')
@csrf_exempt
def payment_success(request,order_id):
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_signature = request.POST.get("razorpay_signature")
    
    client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRETS))

    try:
        payment_check=client.utility.verify_payment_signature({
            'razorpay_order_id': 34344,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        
        if payment_check:
            order = Order.objects.get(order_id=order_id)
            order.paid = True
            order.save()

            cart = Cart.objects.get(id=request.session.get('cart_id'))
            for cartitems in cart.cartitem_set.all():
                cartitems.delete()   


            total = 0
            for order_item in order.orderitem_set.all():
                total += order_item.quantity * order_item.product.product_price

            email_body = render_to_string('email.html',{'orders':order.orderitem_set.all(),'total':total})


            # Send confirmation email
            send_mail(
                'Order payment successful',
                email_body,
                settings.EMAIL_HOST_USER,
                ['swayamharawade0604@gmail.com', request.user.email],
                fail_silently=False,
                html_message=email_body
            )
    except SignatureVerificationError:
        send_mail(
                        'Order payment Failed',
                        f'''Your order {order.order_id} has failed. \n
                        {len(order.orderitem_set.all())} items were attempted to be ordered. \n
                        Please try again later.''',
                        settings.EMAIL_HOST_USER,
                        ['swayamharawade0604@gmail.com', request.user.email],
                        fail_silently=False,
                    )
        return render(request,"payment_failed.html")
            

    order= Order.objects.get(order_id=order_id)
    
    return render(request,"payment_success.html",{"order":order,'total':total})


@login_required(login_url='/login')
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render (request,"order.html",{"orders":orders})