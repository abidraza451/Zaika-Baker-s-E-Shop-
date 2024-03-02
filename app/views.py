from django.shortcuts import render, redirect
from django.db.models import Count
from django.views import View
from . models import Product, Cart, Customer, OrderPlaced, Payment, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.db.models import Sum
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


@login_required
def home(request):
    totalitem = 0
    wishlitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())


@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())


@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html", locals())


@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values(
            'title')
        return render(request, "app/category.html", locals())


@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(
            category=product[0].category).values('title')
        return render(request, "app/category.html", locals())


@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(
            Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulation! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality,
                           mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, "Congratulation! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html', locals())


@login_required
def address(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        #add = Customer.objects.filter(user=request.user)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(
                request, "Congratulation Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


# @login_required
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)
#     Cart(user=user, product=product).save()

#     messages.success(request, 'Item added to cart successfully.')

#     return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:

        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Quantity of item in cart increased.')
    else:
        messages.success(request, 'Item added to cart successfully.')

    return redirect(request.META.get('HTTP_REFERER', '/'))


# @login_required
# def buy_now(request):
#     user = request.user
#     product_id = request.GET.get('prod_id')
#     product = Product.objects.get(id=product_id)
#     Cart(user=user, product=product).save()
#     return redirect("/cart")

@login_required
def buy_now(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    # Check if the product is already in the cart
    existing_cart_item = Cart.objects.filter(
        user=user, product=product).first()

    if existing_cart_item:
        # If the item already exists, increment the quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # If the item does not exist, add it to the cart
        Cart.objects.create(user=user, product=product)

    messages.success(request, 'Item added to cart successfully.')

    return redirect("/cart")


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount+value
    totalamount = amount+30
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount+value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(
            product=prod_id, user=request.user).first()
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                data = {
                    'quantity': cart_item.quantity,
                    'amount': calculate_amount(request.user),
                    'totalamount': calculate_total_amount(request.user)
                }
            else:
                cart_item.delete()
                data = {
                    'reload_page': True
                }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})


@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')

        cart_item = Cart.objects.get(product=prod_id, user=request.user)
        cart_item.delete()

        # Recalculate total amount after deletion
        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 30

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount+value
        totalamount = famount+30
        razoramount = int(totalamount * 100)
        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR",
                "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        return render(request, 'app/checkout.html', locals())


@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product,
                    quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")


@login_required
def orders(request):
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'messages': "Wishlist Addedd Successfully",
        }
        return JsonResponse(data)


@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'messages': "Wishlist Addedd Successfully",
        }
        return JsonResponse(data)


@login_required
def search(request):
    query = request.GET.get('search')
    totalitem = 0
    wishitem = 0
    not_found = False  # Flag to indicate if no items were found
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(title__icontains=query)
    if not product:  # If no items were found
        not_found = True
    return render(request, "app/search.html", {'product': product, 'totalitem': totalitem, 'wishitem': wishitem, 'not_found': not_found})


@login_required
def show_wishlist(request):
    # Retrieve wishlist items associated with the current user
    user = request.user
    wish = Wishlist.objects.filter(user=user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    # Pass wishlist items to the template
    return render(request, 'app/wishlist.html', locals())


@login_required
def remove_wish(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')

        cart_item = Wishlist.objects.get(product=prod_id, user=request.user)
        cart_item.delete()

        # Return success message
        return JsonResponse({})
