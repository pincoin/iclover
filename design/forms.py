from django import forms
from design import models as design_model
from member import models as member_model
from managing import models as managing_model
from allauth.account.forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = member_model.Profile
        fields = ['code','company','address','business','sectors','tell','tax_bill_mail','phone']


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
