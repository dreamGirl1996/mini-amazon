from django.contrib.auth.models import User
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import amazonApp.web_amazon_pb2 as wapb
from .models import Order, AmazonProduct,AmazonUser,Warehouse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm,ProductSearchForm,TrackPackageForm
import socket
from django.views import generic
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect


backend_addr = 'localhost'
#backend_addr = 'vcm-8302.vm.duke.edu'
backend_port = 6888



def backend_conn():
    print('connect to Backend...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((backend_addr, backend_port))
    return s




# Create your views here.
def home(request):
    return render(request,'amazonApp/home.html')




class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_history.html'
    context_object_name = 'orders'



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('amazon-home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def Send(sock, msg):
    req = msg.SerializeToString()
    _EncodeVarint(sock.send, len(req), None)
    sock.send(req)
    print('send finish')

def searchBar(request):
    return render(request,"search_bar.html")

def matching_prods(request):
    search_st=request.GET['search_st']
    matches = AmazonProduct.objects.filter(product_name__contains=search_st)
    return render(request,'catalogue.html',{'matches':matches})

def buy_product(request):
    if request.method == 'GET':
        prodid=request.GET['prodId']
        return render(request,'buy_product.html',{'prodId':prodid})
    else:
        assert request.method =='POST'
        vals=request.POST
        ups_acc=vals['ups_account'] if 'ups_account' in vals else None
        x,y,n=vals['x'],vals['y'],vals['quantity']
        prod_id = vals['prodId']

        prod=AmazonProduct.objects.get(pk=prod_id)
        prod_name=prod.product_name

        if ups_acc:
            status='await_valid'
        else:
            status='pending'
        time =datetime.now()
        order = Order(user_id=request.user, product_name=prod_name, product_num=n, buyer_x=x,
                      buyer_y=y,order_created_time=time,status=status)  # order create
        if ups_acc:
            order.ups_id=ups_acc
        order.save()

        return render(request,'success.html',{'trackId':order.ship_id})#HttpResponseRedirect(reverse("amazon-home"))




'''
def searchProduct(request):
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            sproduct_name = form.cleaned_data.get('product_name')
            sproduct_num = form.cleaned_data.get('product_num')
            sbuy_x = form.cleaned_data.get('buy_x')
            sbuy_y = form.cleaned_data.get('buy_y')

            #screate_time = datetime.datetime.now()

            order = Order(user_id=request.user,product_name=sproduct_name,product_num=sproduct_num,buyer_x=sbuy_x,
                          buyer_y=sbuy_y) #order create
                          
            order.save()


            # backend_sock = backend_conn()
            #
            #
            # new_request=wapb.WACommand()
            # buf = new_request.create.add()
            # buf.order_id = order.ship_id
            # print(buf.order_id)
            # Send(backend_sock,new_request)#


            #slight adjustment
            #avail_products = AmazonProduct.objects.filter(product_name=sproduct_name,product_quantity__gte=sproduct_num)
            avail_products = AmazonProduct.objects.filter(product_name=sproduct_name)


            context = {'avail_products':avail_products}
            return render(request, 'amazonApp/product_search_item.html', context)
    else:
        form = ProductSearchForm()
    return render(request, 'amazonApp/product_search.html', {'form': form})
'''


def trackProduct(request):
    if request.method == 'POST':
        form = TrackPackageForm(request.POST)
        if form.is_valid():
            tpackage_id = form.cleaned_data.get('order_id')
            find_products = Order.objects.filter(ship_id=tpackage_id)

            context = {'find_products': find_products}
            return render(request, 'amazonApp/trackOrderDetail.html', context)
    else:
        form = TrackPackageForm()
    return render(request, 'amazonApp/trackOrder.html', {'form': form})


class HistoryOrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'history_order.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Order.objects.filter(user_id=user)


def searchBuy(request):
    pass



