from django.urls import path

from . import views
from .views import *
from .controller import wishlist
from .controller.wishlist import index
from store.controller import authview

urlpatterns = [
	#Leave as empty string for base url
	path('login/', views.loginPage,name="login"),
	path('logout/', views.logoutUser,name="logout"),
	#path('login/', authview.loginpage,name="loginpage"),
	#path('register/', views.registerPage,name="register"),
	path('store', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('wishlist/',wishlist.index, name="wishlist"),
	path('',views.collections, name="collections"),
	path('checkout/', views.checkout, name="checkout"),
	path('register/',authview.register, name="register"),
	#path('back',views.back, name='back'),
	path('back', views.HomePageView.as_view(), name='back'),
	#path('back', views.HomePageView.as_view(), name='back'),
	path('payment', views.payment, name='payment'),
	path('charge', views.charge, name='charge'),  # new
	path('detail/<id>/', ProductDetailView.as_view(), name='detail'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),
	path('collections/<str:slug>',views.collectionsview,name="collectionsview"),
	path('collections/<str:cate_slug>/<str:prod_slug>',views.productview,name="productview"),
	#path('product/<slug>/',ProductDetailView.as_view(),name='product'),

    path('api/checkout-session/', create_checkout_session, name='api_checkout_session'),

]