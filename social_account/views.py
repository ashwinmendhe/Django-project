from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from django.contrib import messages


#from .filters import OrderFilter
#####################################################################
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
       

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            #print(form)
            
            if form.is_valid():
                #print(form.is_valid())
                form.save()
            
                user = form.cleaned_data.get('first_name')
                messages.success(request,'Account was created for ' + user)
            
                return redirect('login')
        context = {'form':form}
        return render(request, 'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password incorrect')
                #return render(request, 'accounts/login.html')
        return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

#####################################################################
@login_required(login_url='login')
def home(request):
    orders =Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered= orders.filter(status='Deliverd').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers,
    'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

@login_required(login_url='login')
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer,'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customer.html',context)