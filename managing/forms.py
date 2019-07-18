import json
from django import forms
from django.contrib.auth.models import User
from member import models as member_models
from managing import models as managing_models
from design import models as design_models
from django.db.models import Q

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'이름',
            }
        ),
        help_text='ID :'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
        help_text='PW :'
    )

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
    def __init__(self, *args, **kwargs):
        super(CustomerCreateForm, self).__init__(*args, **kwargs)
        self.fields['code'].required = True
        self.fields['company'].required = True

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
        fields = ['company', 'company_keyword', 'ceo', 'tell', 'address', 'phone', 'confirm', 'manager','division',\
            'options', 'keywords', 'memo', 'sectors', 'business', 'tax_bill_mail', 'address2', 'state_select', 'state'
        ]
        widgets = {
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
            'division': forms.TextInput(attrs={'class': 'form-control', }),
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
            'division': '판매=1 매입=2',
        }
class ProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = User.objects.filter(profile__division=2)
        self.fields['category'].queryset = design_models.Category.objects.filter(level=1)

    class Meta:
        model = design_models.ProductText
        fields = ['category','supplier','standard','horizontal','vertical','width','height',\
                  'paper','gram','color','paper_option','side','etc','etc_option','memo',\
                  'code','title','sell_price','buy_price','quantity','main_quantity'
                  ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'standard': forms.TextInput(attrs={'class': 'form-control','placeholder':'예) a4 [4000장], b5 [8000장] , 상의, 하의'}),
            'horizontal': forms.TextInput(attrs={'class': 'form-control','type':'number',' step':'0.001'}),
            'vertical': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'width': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'paper': forms.TextInput(attrs={'class': 'form-control','placeholder':'예) 아트지, 2445, 물비누'}),
            'gram': forms.TextInput(attrs={'class': 'form-control','placeholder':'예) 150g , 18kg, XXL'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'paper_option': forms.TextInput(attrs={'class': 'form-control'}),
            'side': forms.TextInput(attrs={'class': 'form-control'}),
            'etc': forms.TextInput(attrs={'class': 'form-control'}),
            'etc_option': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'type': 'number','placeholder':'예) 품목 번호'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sell_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'buy_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'main_quantity': forms.CheckboxInput(attrs={'style': "width:100px;,height:100px;"}),
        }

class ProductUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].queryset = User.objects.filter(profile__division=2)
        self.fields['category'].queryset = design_models.Category.objects.filter(level=1)

    class Meta:
        model = design_models.ProductText
        fields = ['category', 'supplier', 'standard', 'horizontal', 'vertical', 'width', 'height', \
                  'paper', 'gram', 'color', 'paper_option', 'side', 'etc', 'etc_option', 'memo', \
                  'code', 'title', 'sell_price', 'buy_price', 'quantity', 'main_quantity'
                  ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'standard': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '예) a4 [4000장], b5 [8000장] , 상의, 하의'}),
            'horizontal': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'vertical': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'width': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'height': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'paper': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예) 아트지, 2445, 물비누'}),
            'gram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예) 150g , 18kg, XXL'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'paper_option': forms.TextInput(attrs={'class': 'form-control'}),
            'side': forms.TextInput(attrs={'class': 'form-control'}),
            'etc': forms.TextInput(attrs={'class': 'form-control'}),
            'etc_option': forms.TextInput(attrs={'class': 'form-control'}),
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': '예) 사업자번호'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sell_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'buy_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', ' step': '0.001'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'main_quantity': forms.CheckboxInput(attrs={'style': "width:100px;,height:100px;"}),
        }

class SampleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SampleCreateForm, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = User.objects.filter(is_staff=True)
        self.fields['category'].queryset = design_models.Category.objects.filter(level=1)

    class Meta:
        model = managing_models.Sample
        fields = ['category','sectors_category','employees','name','keyword','images']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control','required':'' }),
            'sectors_category': forms.Select(attrs={'class': 'form-control'}),
            'employees': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'keyword': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'images': forms.FileInput(attrs={'class':'form-control','required':'' })
        }

class SampleUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SampleUpdateForm, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = User.objects.filter(is_staff=True)
        self.fields['category'].queryset = design_models.Category.objects.filter(level=1)

    class Meta:
        model = managing_models.Sample
        fields = ['category', 'sectors_category', 'employees', 'name', 'keyword', 'images','state']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sectors_category': forms.Select(attrs={'class': 'form-control'}),
            'employees': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'keyword': forms.TextInput(attrs={'class': 'form-control','autocomplete': "off"}),
            'images': forms.FileInput(attrs={'class': 'form-control'}),
            'state':forms.CheckboxInput(attrs={ 'style':"width:50px;,height:50px;"})
        }

class AskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AskCreateForm, self).__init__(*args, **kwargs)
        self.fields['ask_to'].queryset = User.objects.filter(is_staff=True)

    class Meta:
        model = managing_models.Ask
        fields = ['ask_to','ask_what','ask_part']
        widgets = {
            'ask_to': forms.Select(attrs={'class': 'form-control'}),
            'ask_what': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': "off"}),
            'ask_part': forms.Select(attrs={'class': 'form-control'}),
        }


class AskUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AskUpdateForm, self).__init__(*args, **kwargs)
        self.fields['ask_to'].queryset = User.objects.filter(is_staff=True)

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
            'name': forms.TextInput(attrs={'class': 'form-control','required':''}),
            'bank': forms.TextInput(attrs={'class': 'form-control','required':''}),
            'amount': forms.TextInput(attrs={'type': 'number','class': 'form-control'}),
            'part': forms.TextInput(attrs={'type':'hidden'}),
             }

class DepositUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Deposit
        fields = ['memo','bill','state']
        widgets = {
            'memo': forms.TextInput(attrs={'class': 'form-control'}),
            'bill': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class OrderWithDepositCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderWithDepositCreateForm, self).__init__(*args, **kwargs)
        self.fields['order'].required = False
        self.fields['deposit'].required = False
        self.fields['delete'].required = False
        self.fields['balance'].required = False
        self.fields['division'].required = False

    order = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'hidden',
            }
        ),
        help_text='주문 :'
    )
    deposit = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'hidden',
            }
        ),
        help_text='입금 :'
    )
    delete = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'hidden',
            }
        ),
        help_text='삭제 리스트 :'
    )
    balance = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'hidden',
            }
        ),
        help_text='차액 :'
    )
    division = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='분할 :'
    )

class OrderWithImagesCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderWithImagesCreateForm, self).__init__(*args, **kwargs)

    pro_image = forms.FileInput()

class EmployeesCreateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Employees
        fields = ['name','cellphone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' }),
            'cellphone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EmployeesUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Employees
        fields = ['name', 'cellphone','state','join','leave','join_pic','leave_pic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','type':'hidden'}),
            'cellphone': forms.TextInput(attrs={'class': 'form-control'}),
            'join': forms.DateInput(attrs={'class': 'form-control','placeholder':'0000-00-00'}),
            'leave': forms.DateInput(attrs={'class': 'form-control','placeholder':'0000-00-00'}),

        }


class MemoCreateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Memo
        fields = ['content','importance']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'importance': forms.CheckboxInput(attrs={ 'style':"width:50px;,height:50px;"}),
        }
        help_texts = {
            'content': '내용',
            'importance': '중요도 체크',
        }



class MemoUpdateForm(forms.ModelForm):
    class Meta:
        model = managing_models.Memo
        fields = ['content','importance','common','confirm','employees']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
            'importance': forms.CheckboxInput(attrs={ 'style':"width:50px;,height:50px;"}),
            'common': forms.CheckboxInput(attrs={'style': "width:50px;,height:50px;"}),
            'confirm': forms.CheckboxInput(attrs={'style': "width:50px;,height:50px;"}),
            'employees': forms.TextInput(attrs={'type': "hidden"}),
        }
        help_texts = {
            'content': '내용',
            'importance': '중요도 체크',
            'common': '공유',
            'confirm': '종료',
        }

class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['company_keyword'].required = False
        self.fields['order_date'].required = False
        self.fields['manager'].required = False
        self.fields['option'].required = False
        self.fields['confirm'].required = False
        self.fields['memo'].required = False
        self.fields['fix_manager'].required = False
        self.fields['in_memo'].required = False
        self.fields['out_memo'].required = False
        self.fields['address'].required = False
        self.fields['tell'].required = False
        self.fields['tax'].required = False
        self.fields['code'].required = False


    company = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='상호명 :'
    )
    company_keyword = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='키워드 :'
    )
    manager =  forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='작업자 :'
    )
    option = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='결재/포함/택배 :'
    )
    confirm = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='시안확인 :'
    )
    memo = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
            }
        ),
        help_text='거래처 정보 :'
    )
    in_memo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='관리자 메모 :'
    )
    out_memo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='고객 노출 메모 :'
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='주소 :'
    )
    code = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden', }), )
    fix_manager = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden', }), )
    tell = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden', }), )
    joo_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    order_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    json_data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    tax = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    state = forms.CharField()

class SpecialPriceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SpecialPriceForm, self).__init__(*args, **kwargs)

    customer = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': "hidden"
            }
        ),
        help_text='업체 :'
    )
    product = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': "hidden"
            }
        ),
        help_text='품목 :'
    )
    new_price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text='새로운 가격 :'
    )
