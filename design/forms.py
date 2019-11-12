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
        self.fields['file'].required = False
        self.fields['text'].required = False

    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'pis','onchange':'readURL(this);','style':'display: none;'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'style':'display: none;'}))

    def clean_file(self):
        content = self.cleaned_data['file']
        if content:
            content_name = content.name.split('.')[-1]
            invalid_list = ['css','js','c','cpp','py','php','exe','bat','reg','vbs','swf','jar','html']
            if content_name in invalid_list:
                raise forms.ValidationError(f'.{content_name} 파일은 업로드 하실 수 없습니다')
        return content

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
