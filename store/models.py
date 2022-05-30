from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
import datetime
import os


# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

DELIVERY_TYPE=(
	(0, ''),
    (1, 'Free delivery'),
)

def get_file_path(request, filename):

	original_filename = filename
	nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M-%S')
	filename = "%s%s" % (nowTime, original_filename)
	return os.path.join('uploads/', filename)

class Catergory(models.Model):

	slug = models.CharField(max_length=150, null=False, blank = False)
	name = models.CharField(max_length=200, null=False, blank = False)
	image = models.ImageField(upload_to=get_file_path,null=True, blank = True)
	description = models.TextField(null=True, blank = True)
	status =  models.BooleanField(default=False,help_text="0=default, 1=Hidden")
	trending = models.BooleanField(default=False,help_text="0=default, 1=Hidden")
	meta_title = models.CharField(max_length=150, null=False, blank = False)
	meta_keywords = models.CharField(max_length=150, null=False, blank = False)
	meta_description = models.TextField(max_length=500,null=False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	category = models.ForeignKey(Catergory,default=False, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	description = models.TextField(max_length=500, null=True)
	small_description = models.TextField(max_length=250,null=False, blank=False,default=False)
	delivery_type = models.IntegerField(choices=DELIVERY_TYPE,blank=True,null=True)
	status =  models.BooleanField(default=False,help_text="0=default, 1=Hidden")
	image_main = models.ImageField(upload_to=get_file_path,null=True, blank=True)
	image1 = models.ImageField(upload_to=get_file_path,null=True, blank=True)
	image2 = models.ImageField(upload_to=get_file_path,null=True, blank=True)
	image3 = models.ImageField(upload_to=get_file_path,null=True, blank=True)
	slug = models.CharField(max_length=150, null=False, blank=False)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class ProductList(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	

	def __str__(self):
		return self.name




class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

class Wishlist(models.Model):

	user = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)