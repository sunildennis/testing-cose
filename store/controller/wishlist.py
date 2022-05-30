from multiprocessing import context
from re import I
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from ..models import * 
from django.http import HttpResponse
from ..utils import cookieCart, cartData, guestOrder
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
from ..models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic.base import TemplateView
from django.core.mail import send_mail



def index(request):

    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, 'store/wishlist.html',context)



