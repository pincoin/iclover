from django import forms
from design import models as design_model
from member import models as member_model
from managing import models as managing_model
from allauth.account.forms import LoginForm

class MyCustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = member_model.Profile
        fields = ['code','company','address','business','sectors','tell','tax_bill_mail','phone']


class ProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    sector =  forms.ModelChoiceField(queryset=design_model.SectorsCategory.objects.all())

