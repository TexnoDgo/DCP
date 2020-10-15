from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Assortment, Detail, Project, Order, Position, City, Manufactured, Operation, Transaction, blog


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']


'''class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title']'''


class AssortmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assortment
        fields = ['title']


class DetailCreateForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['title', 'draw_pdf', 'material', 'assortment', 'thickness_diameter']


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'project', 'readiness']


class OrderSuperCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table']


class OrderDRAWUploadForm(forms.Form):
    archive = forms.FileField()
    flag = forms.BooleanField(required=False, initial=False)
    fields = ['archive', 'flag']


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['order', 'detail', 'quantity']


class PositionStorageForm(forms.Form):
    position_in = forms.CharField(max_length=50)
    fields = ['position_in']
    

class PositionDrawAdd(forms.Form):
    draw = forms.FileField()
    fields = ['draw']

class PasitionAddForm(forms.Form):
    detail_title = forms.CharField(max_length=50)
    quantity = forms.CharField(max_length=10)
    material = forms.CharField(max_length=50)
    assortment = forms.CharField(max_length=50)
    thickness_diameter = forms.CharField(max_length=10)
    
    fields = ['detail_title', 'quantity', 'material', 'assortment', 'thickness_diameter']


class PositionSearch(forms.Form):
    my_request = forms.CharField(max_length=50)
    fields = ['my_request']


class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['title']


class ManufacturedCreateForm(forms.ModelForm):
    class Meta:
        model = Manufactured
        fields = ['title', 'city']


class OperationCreateForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['manufactured']


class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['ready_quantity']


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class blog_create_form(forms.ModelForm):

    class Meta:
        model = blog
        fields = ['title', 'text']
        
