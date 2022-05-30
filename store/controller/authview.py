from multiprocessing import context
from re import I
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from store.models import * 
from django.http import HttpResponse
from store.utils import cookieCart, cartData, guestOrder
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
from store.models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from store.forms import CustomUserForm



def register(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Registration successfully! Login to continue' )
            return redirect('/login')
    context = {'form':form}
    return render(request, 'store/auth/register.html',context)

def loginpage(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=name, password=password)

        if user is not None:

            login(request, user)
            messages.success(request,"logged in successfully")
            return redirect('store')
        
        else:

            messages.error(request,"Invalid username or password")

            return redirect('loginpage')

    return render(request, 'store/auth/login.html')