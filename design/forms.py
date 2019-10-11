from django import forms
from design import models as design_model
from member import models as member_model
from managing import models as managing_model
from allauth.account.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control' ,'readonly':'readonly'})
        self.fields['address2'].widget.attrs.update({'class': 'form-control' ,'readonly':'readonly'})
        self.fields['address_detail'].widget.attrs.update({'class': 'form-control'})
        self.fields['address_option'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['bill_select'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = member_model.CustomerProfile
        fields = ['company','code','phone','address','address2','address_detail','address_option','bill_select']

class CustomerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control' ,'readonly':'readonly'})
        self.fields['address2'].widget.attrs.update({'class': 'form-control' ,'readonly':'readonly'})
        self.fields['address_detail'].widget.attrs.update({'class': 'form-control'})
        self.fields['address_option'].widget.attrs.update({'class': 'form-control'})
        self.fields['business'].widget.attrs.update({'class': 'form-control'})
        self.fields['sectors'].widget.attrs.update({'class': 'form-control'})
        self.fields['tell'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['tax_bill_mail'].widget.attrs.update({'class': 'form-control'})
        self.fields['ceo'].widget.attrs.update({'class': 'form-control'})
        self.fields['bill_select'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = member_model.CustomerProfile
        fields = ['code','company','address','address2','address_detail','address_option','business','sectors',
                  'tell','tax_bill_mail','phone','ceo','bill_select']

class ProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    sector =  forms.ModelChoiceField(queryset=design_model.SectorsCategory.objects.all())

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class SampleSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SampleSearchForm, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = User.objects.filter(is_staff=True)
        self.fields['category'].queryset = design_model.Category.objects.filter(level=1)

    class Meta:
        model = managing_model.Sample
        fields = ['category','sectors_category','name','keyword','images']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control' }),
            'sectors_category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'images': forms.FileInput(attrs={'class':'form-control'})
        }
