"""amazon_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from amazonApp import views as amazonapp_views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('amazonApp.urls')),
    path('amazon/', include('amazonApp.urls')),
    path('register/',amazonapp_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('search/', amazonapp_views.searchBar, name='search'),
    path('allOrder/<int:pk>/', amazonapp_views.HistoryOrderListView.as_view(), name='allOrder'),
    path('track/', amazonapp_views.trackProduct, name='track'),
    path('matching_prods/',amazonapp_views.matching_prods,name='matching_prods'),
    path('buy_product/',amazonapp_views.buy_product,name='buy_product')
    #path('search/query/')

]
