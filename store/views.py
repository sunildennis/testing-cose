from multiprocessing import context
from re import I
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.http import HttpResponse
from .utils import cookieCart, cartData, guestOrder
from django.views import View
import stripe
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView




from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


from django.views.generic.base import TemplateView

from django.core.mail import send_mail

# def HomePageView(request):

# 	return render(request, 'store/home.html')

class HomePageView(TemplateView):
    template_name = 'store/thankyou.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLIC_KEY
        return context

def collections(request):

	category = Catergory.objects.filter(status=0)

	context = {'category':category}

	return render(request, 'store/collections.html', context)


def nav(request):

	return render(request, 'store/navbar.html')




def payment(request):

	if request.method == 'POST':

		if 'mail' in request.POST:

			name = request.POST.get('naame')
			email = request.POST.get('emaail')
			fromemail = settings.EMAIL_HOST_USER

			send_mail(
				'Subject',
				'Here is the message.',
				fromemail,
				[email],
				fail_silently=False,
			)

	return render(request, 'store/charge.html')


stripe.api_key = settings.STRIPE_SECRET_KEY

def charge(request): # new

    return render(request, 'store/charge.html')

def loginPage(request):
	
	page = 'login'

	if request.user.is_authenticated:
		return redirect('/')
	if request.method == 'POST':
		username = request.POST.get('username').lower()
		password = request.POST.get('password')

		try:
			user = User.objects.get(username=username)

		except:
			messages.error(request,'User not found')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')

		else:
			messages.error(request,'Username or password does not exists')


	context = {'page':page}
	return render(request, 'store/login_registration.html',context)

def logoutUser(request):
	logout(request)
	return redirect('/')

def registerPage(request):
	
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			login(request,user)
			return redirect('/')

		else:
			messages.error(request,'An error occured during registration')

	return render(request, 'store/login_registration.html',{'form':form})


def store(request):
	q = request.GET.get('q') if request.GET.get('q') != None else ''

	products = Product.objects.filter(name__icontains=q)
	
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	producty_name  = Product.objects.all()
	products_count = products.count()

	if request.method == 'POST':

		# if 'mail' in request.POST:

		email = request.POST['nemail']
		fromemail = settings.EMAIL_HOST_USER
		message = f'Hello from now you will receive all the newsletters'

		send_mail(
			'Newsletter',
			message,
			fromemail,
			[email],
			fail_silently=False,
		)

		return redirect('store')



	context = {'products':products, 'cartItems':cartItems,'products_count':products_count,'producty_name':producty_name}
	return render(request, 'store/store.html', context)

def collectionsview(request, slug):

	q = request.GET.get('q') if request.GET.get('q') != None else ''

	products = Product.objects.filter(name__icontains=q)
	
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	producty_name  = Product.objects.all()
	products_count = products.count()

	if(Catergory.objects.filter(slug=slug, status=0)):

		productss = Product.objects.filter(category__slug=slug)

		category_name = Catergory.objects.filter(slug=slug).first()

		context = {'productss':productss,'category_name':category_name,'cartItems':cartItems,'products':products,'order':order,'items':items}

		return render(request, 'store/products.html',context)

	else:

		messages.warning(request, 'No such')
		return redirect('store')


def productview(request, cate_slug, prod_slug):

	q = request.GET.get('q') if request.GET.get('q') != None else ''

	products = Product.objects.filter(name__icontains=q)
	
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	producty_name  = Product.objects.all()
	products_count  = products.count()

	if(Catergory.objects.filter(slug=cate_slug, status=0)):
		if(Product.objects.filter(slug=prod_slug, status=0)):

			products = Product.objects.filter(slug=prod_slug, status=0).first

		#product_name = Product.objects.filter(slug=slug).first()

			context = {'products':products,'cartItems':cartItems,'products':products,'order':order,'items':items}

		else:
			messages.error(request,"No such product")
			return redirect('store')
	else:

		messages.warning(request, 'No such category')
		return redirect('store')
	
	return render(request, 'store/product.html',context)




def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

# @login_required(login_url='login')
# def wishlist(request):

# 	wishlist = Wishlist.objects.all()
# 	context = {'wishlist':wishlist}
# 	return render(request, 'store/wishlist.html',context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']



	#itemprice = order.get('get_cart_total')
	
	address = request.POST.get('address')
	city = request.POST.get('city')
	state = request.POST.get('state')
	country = request.POST.get('country')
	zipcode = request.POST.get('zipcode')

	if request.method == 'POST':
		name = request.POST.get('naame')
		email = request.POST.get('emaail')
		adres  = address
		fromemail = settings.EMAIL_HOST_USER
		message = f'Hello {name} from {adres} your order has been confirmed'

		send_mail(
			'Order Confirmed',
			message,
			fromemail,
			[email],
			fail_silently=False,
		)

		return redirect('back')

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def back(request):
	
	return render(request, 'store/thankyou.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  

@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    order = Order()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"

class OrderHistoryListView(ListView):
    model = Order
    template_name = "payments/order_history.html"
