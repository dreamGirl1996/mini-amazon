from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AmazonUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProductSearchForm(forms.Form):
    product_name = forms.CharField()
    #product_num = forms.IntegerField()
    #buy_x=forms.IntegerField()
    #buy_y=forms.IntegerField()

class BuyProductForm(forms.Form):
    product_num = forms.IntegerField()
    ups_acc=forms.CharField()
    buy_x=forms.IntegerField()
    buy_y=forms.IntegerField()

class TrackPackageForm(forms.Form):
    order_id = forms.IntegerField(help_text="Your order ID")
