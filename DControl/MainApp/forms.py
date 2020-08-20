from django import forms
from .models import Material, Assortment, Detail, Project, Order, Position, City, Manufactured, Operation, Transaction


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']


class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title']


class AssortmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assortment
        fields = ['title']


class DetailCreateForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['title', 'draw_pdf', 'material', 'assortment']


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
        fields = ['title', 'manufactured', 'position', 'remaining_parts']


class TransactionCreateForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['ready_quantity']
