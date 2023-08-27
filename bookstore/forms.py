from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Order,Customer,Book
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ='__all__'


class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']      
        

class Customerform(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','status']

# class register(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']

class Bookform(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'        
'''  
class OredFormset(ModelForm):
    class Meta :
        model : Order
        fileds ='__all__'        
'''