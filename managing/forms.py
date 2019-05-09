from django import forms
from member import models as member_models
from managing import models as managing_models
from design import models as design_models

class DataSearchForm(forms.Form):
    q = forms.CharField(
        label=('search word'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '검색어를 입력해주세요',
                'autocomplete': "off",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q', '')
        super(DataSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].initial = q
        self.fields['q'].required = False


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = member_models.Profile
        fields = [
            'code','company', 'company_keyword','ceo','tell','address','phone','confirm','manager',\
            'options','keywords','memo','sectors','business','tax_bill_mail','address2'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control','type':'number'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'company_keyword': forms.TextInput(attrs={'class': 'form-control'}),
            'ceo': forms.TextInput(attrs={'class': 'form-control'}),
            'tell': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'confirm': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.TextInput(attrs={'class': 'form-control'}),
            'options': forms.TextInput(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'sectors': forms.TextInput(attrs={'class': 'form-control'}),
            'business': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_bill_mail': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'code':'사업자번호 -숫자만',
            'company': '업체명',
            'company_keyword': '검색창 내용 /키워드',
            'ceo': '대표자',
            'tell': '전화번호',
            'address': '주소1',
            'address2': '주소2',
            'phone': '주문자 정보',
            'confirm': '시안 확인',
            'manager': '담당 직원',
            'options': '결제/포함/택배',
            'keywords': '후가공/메모',
            'memo': '적요 *세금계산서 or 현금영수증',
            'sectors': '업종',
            'business': '업태',
            'tax_bill_mail': '이메일',
        }
        error_messages = {
            'user': {
                'invalid': "유효하지 않습니다.",
                'unique': "이미 프로필이 등록되어있습니다.",
            },
            'code': {
                'invalid': "사업자번호는 숫자만 입력하셔야합니다.",
                'unique': "사업자 번호가 이미 존재합니다.",
            },
        }

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = member_models.Profile
        fields = [
            'code', 'company', 'company_keyword', 'ceo', 'tell', 'address', 'phone', 'confirm', 'manager',\
            'options', 'keywords', 'memo', 'sectors', 'business', 'tax_bill_mail', 'address2', 'state_select', 'state'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control','type':'hidden'}),
            'company': forms.TextInput(attrs={'class': 'form-control',}),
            'company_keyword': forms.TextInput(attrs={'class': 'form-control',}),
            'ceo': forms.TextInput(attrs={'class': 'form-control',}),
            'tell': forms.TextInput(attrs={'class': 'form-control',}),
            'address': forms.TextInput(attrs={'class': 'form-control',}),
            'address2': forms.TextInput(attrs={'class': 'form-control',}),
            'phone': forms.TextInput(attrs={'class': 'form-control',}),
            'confirm': forms.TextInput(attrs={'class': 'form-control',}),
            'manager': forms.TextInput(attrs={'class': 'form-control',}),
            'options': forms.TextInput(attrs={'class': 'form-control',}),
            'keywords': forms.TextInput(attrs={'class': 'form-control',}),
            'memo': forms.TextInput(attrs={'class': 'form-control',}),
            'sectors': forms.TextInput(attrs={'class': 'form-control',}),
            'business': forms.TextInput(attrs={'class': 'form-control',}),
            'tax_bill_mail': forms.TextInput(attrs={'class': 'form-control',}),
            'state_select': forms.Select(attrs={'class': 'form-control' }),
            'state': forms.TextInput(attrs={'class': 'form-control',  }),
        }
        help_texts = {
            'code':'사업자번호 -숫자만',
            'company': '업체명',
            'company_keyword': '검색창 내용 /키워드',
            'ceo': '대표자',
            'tell': '전화번호',
            'address': '주소1',
            'address2': '주소2',
            'phone': '주문자 정보',
            'confirm': '시안 확인',
            'manager': '담당 직원',
            'options': '결제/포함/택배',
            'keywords': '후가공/메모',
            'memo': '적요 *세금계산서 or 현금영수증',
            'sectors': '업종',
            'business': '업태',
            'tax_bill_mail': '이메일',
            'state_select': '사업자 상태',
            'state': '폐업일자',
        }
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = design_models.ProductBase
        fields = '__all__'

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = design_models.ProductBase
        fields = ['code']

class SampleCreateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Sample
        fields = ['category','sectors_category','employees','name','keyword','sample_img']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control' }),
            'sectors_category': forms.Select(attrs={'class': 'form-control'}),
            'employees': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'keyword': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'sample_img': forms.FileInput(attrs={'class':'form-control'})
        }

class SampleUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Sample
        fields = ['category', 'sectors_category', 'employees', 'name', 'keyword', 'sample_img','state']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sectors_category': forms.Select(attrs={'class': 'form-control'}),
            'employees': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'keyword': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'sample_img': forms.FileInput(attrs={'class': 'form-control'}),
            'state':forms.CheckboxInput(attrs={ 'style':"width:50px;,height:50px;"})
        }

class AskCreateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Ask
        fields = ['ask_to','ask_what','ask_part']
        widgets = {
            'ask_to': forms.Select(attrs={'class': 'form-control'}),
            'ask_what': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'ask_part': forms.Select(attrs={'class': 'form-control'}),
        }



class AskUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Ask
        fields = ['ask_to', 'ask_what', 'ask_part','ask_finish']
        widgets = {
            'ask_to': forms.Select(attrs={'class': 'form-control'}),
            'ask_what': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'ask_part': forms.Select(attrs={'class': 'form-control'}),
            'ask_finish': forms.CheckboxInput(attrs={'style': "width:100px;,height:100px;"})
        }

class DepositCreateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Deposit
        fields = ['bank','name','amount','part']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.TextInput(attrs={'type': 'number','class': 'form-control'}),
            'part': forms.TextInput(attrs={'type':'hidden'}),
             }

class DepositUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Deposit
        fields = ['memo','bill']
        widgets = {
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'bill': forms.TextInput(attrs={'class': 'form-control'}),
        }
