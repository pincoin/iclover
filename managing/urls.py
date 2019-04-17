from django.urls import path
from .views import Main, CustomerView, ProductView, SampleView, CategoryView, DiscountView, Deal_listView, DemandView

app_name = 'managing'

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('customer', CustomerView.as_view(), name='customer'),
    path('product', ProductView.as_view(), name='product'),
    path('sample', SampleView.as_view(), name='sample'),
    path('category', CategoryView.as_view(), name='category'),
    path('discount', DiscountView.as_view(), name='discount'),
    path('deal_list', Deal_listView.as_view(), name='deal_list'),
    path('demand', DemandView.as_view(), name='demand'),


]