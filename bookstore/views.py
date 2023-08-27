from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout #added
from .models import *
from .forms import OrderForm,Customerform ,Bookform,CreateNewUser #added
from django.forms import inlineformset_factory
from django.contrib import messages
# from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm  # creation login and registers
from django.contrib.auth import authenticate , login , logout

from django.contrib.auth.decorators import login_required

from .decorators import notLoggedUsers,allowedUsers,forAdmins
from .filters import *

from django.contrib.auth.models import Group

import requests

from django.conf import settings


# Create your views here.

#-------------------------------------------------------------
@login_required(login_url='/login')  # login before acc in page home 
# @allowedUsers(allowedGroups=['admin'])
@forAdmins
def home(request):
    customers =Customer.objects.all()
    orders=Order.objects.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progress').count()
    out_orders = orders.filter(status='out of order').count()
    context = {'customers': customers ,
               'orders': orders,
               't_orders': t_orders,
               'p_orders': p_orders,
               'd_orders': d_orders,
               'in_orders': in_orders,
               'out_orders': out_orders}
    return render(request,'bookstore/dashboard.html',context)


@login_required(login_url='/login') 
def books(request):
    books =Book.objects.all()
    return render(request,'bookstore/books.html',{'books':books})
#---------------------------------------------------

#---------------------------------------------------

#---------------------------------------------------
@login_required(login_url='/login') 
@allowedUsers(allowedGroups=['admin'])
def customer(request,pk):
    customer =Customer.objects.get(id=pk)
    order = customer.order_set.all()
    number_orders=order.count()
    serchFilter = OrderFilter(request.GET,queryset=order)
    order = serchFilter.qs
    context = {'customer': customer ,
               'order': order,
               'number_orders':number_orders,
               'myfilter':serchFilter}
    return render(request,'bookstore/customer.html',context)
#-----------------------------------------------------
@login_required(login_url='/login')
@allowedUsers(allowedGroups=['admin'])
def create(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book','status'),extra=2)   # extra Ar ==> nomber of requestes (order or orders)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance=customer)
    #form  = OrderForm()
    if request.method == 'POST':
        print(request.POST)
        #form  = OrderForm(request.POST)
        formset = OrderFormSet(request.POST ,instance=customer)
        if formset.is_valid():
           formset.save() 
           return redirect('/')
    #context = {'form':form}    
    context = {'formset':formset}
    return render(request,'bookstore/my_order_form.html',context)

#------------------------------------------------------------
@login_required(login_url='/login') 
@allowedUsers(allowedGroups=['admin'])
def update(request,pk): 
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) 
    if request.method == 'POST': 
       form = OrderForm(request.POST, instance=order)
       if form.is_valid():
           form.save()
         
           return redirect('/')

    context = {'form':form}

    return render(request , 'bookstore/my_order_form.html', context )

#-------------------------------------------------------------
@login_required(login_url='/login')
@allowedUsers(allowedGroups=['admin'])
def delete(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request,'bookstore/delelt_form.html',context)

#-------------------------------------------------------------
@notLoggedUsers
def userlogin(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Not exist user')
    return render(request,'bookstore/login.html')

#-------------------------------------------------------------
def userlogout(request):
    logout(request)
    return redirect('/login')    

#-------------------------------------------------------------
def register(request):
    #---------------------
    msg = "invalid"
    msg_invalid = False
    #---------------------
    form = CreateNewUser()   # object forms
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            #-------
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret' :settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                user = form.save() 
                username = form.cleaned_data.get('username') # msg create user go to login page
                messages.success(request, username + " Created Successfuly ! ")
                return  redirect("/login")
            else:
                msg_invalid = True
                #messages.error(request," invalid Recaptcha please try again ! ",)
            #-------
            # add group to -> decorators.py
            # group = Group.objects.get(name="customer")
            # user.groups.add(group)
            #-------
    if msg_invalid == True :
        context = { 'form': form,'msg':msg}      
    else :
        context = { 'form': form}

    return render(request,'bookstore/register.html',context)

#---------------------add book----------------------
@login_required(login_url='/login')
@allowedUsers(allowedGroups=['admin'])
def addbook(request):
    form = Bookform()
    if request.method == 'POST':
        form = Bookform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}    
    return render(request,'bookstore/addbook.html',context)

#-------------------------------------------------------------
@login_required(login_url='/login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):
    orders = request.user.customer.order_set.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progress').count()
    out_orders = orders.filter(status='out of order').count()
    context = {
               'orders': orders,
               't_orders': t_orders,
               'p_orders': p_orders,
               'd_orders': d_orders,
               'in_orders': in_orders,
               'out_orders': out_orders}
    return render(request,'bookstore/profile.html',context)
    

#-------------------------------------------------------------
@login_required(login_url='/login')
def profileInfo(request):
    customer = request.user.customer
    form= Customerform(instance=customer)
    if request.method == 'POST': 
       form = Customerform(request.POST,request.FILES, instance=customer)
       if form.is_valid():
           form.save()
           return redirect('/profile')
    context = {'form':form}
    return render(request,'bookstore/profile_info.html',context)
    