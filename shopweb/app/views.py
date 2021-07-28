from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem = 0
        Mobile=Product.objects.filter(category = 'M')
        Laptop=Product.objects.filter(category = 'L')
        HeadPhone=Product.objects.filter(category = 'HP')
        WomenDress=Product.objects.filter(category = 'WD')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'Mobile':Mobile,'Laptop':Laptop,'HeadPhone':HeadPhone,
        'WomenDress':WomenDress,'totalitem' : totalitem})
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id ) &  Q(user=request.user)).exists()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart' : item_already_in_cart,'totalitem' : totalitem})


@login_required
def add_to_cart(request):
    user=request.user
    product_id= request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity * p.product.discount_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount,'totalitem' : totalitem})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',{'order_placed':op})

def mobile(request,data=None):
    totalitem = 0
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi'or data=='Iphone':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discount_price__lt=10000)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles':mobiles,'totalitem' : totalitem})
def laptop(request,data=None):
    totalitem = 0
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Dell'or data=='Lenovo':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discount_price__lt=5000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discount_price__gt=5000)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html', {'laptops':laptops,'totalitem' : totalitem})
def headphone(request,data=None):
    totalitem = 0
    if data == None:
        headphone = Product.objects.filter(category='HP')
    elif data == 'Sony'or data=='JBL':
        headphone = Product.objects.filter(category='HP').filter(brand=data)
    elif data == 'below':
        headphone = Product.objects.filter(category='HP').filter(discount_price__lt=500)
    elif data == 'above':
        headphone = Product.objects.filter(category='HP').filter(discount_price__gt=500)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/headphone.html', {'headphone':headphone,'totalitem' : totalitem})
def dress(request,data=None):
    totalitem = 0
    if data == None:
        dress = Product.objects.filter(category='WD')
    elif data == 'Dress':
        dress = Product.objects.filter(category='WD').filter(brand=data)
    elif data == 'below':
        dress = Product.objects.filter(category='WD').filter(discount_price__lt=500)
    elif data == 'above':
        dress = Product.objects.filter(category='WD').filter(discount_price__gt=500)
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/dresses.html', {'dress':dress,'totalitem' : totalitem})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem' : totalitem})
    def post(self,request):
        totalitem = 0
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg= Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem' : totalitem})
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/address.html',{'add':add,'active':'btn-primary','totalitem' : totalitem})


@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem' : totalitem})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    
