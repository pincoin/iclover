from django.urls import path
from . import views

app_name = 'managing'

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer_result/', views.CustomerResultView.as_view(), name='customer_result'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('product/create/', views.ProdcutCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('sample/', views.SampleView.as_view(), name='sample'),
    path('sample/create/', views.SampleCreateView.as_view(), name='sample_create'),
    path('sample/<int:pk>/update/', views.SampleUpdateView.as_view(), name='sample_update'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('discount/', views.DiscountView.as_view(), name='discount'),
    path('deal_list/', views.Deal_listView.as_view(), name='deal_list'),
    path('demand/', views.DemandView.as_view(), name='demand'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('deposit/create/', views.DepositCreateView.as_view(), name='deposit_create'),
    path('deposit/<int:pk>/update/', views.DepositUpdateView.as_view(), name='deposit_update'),
    path('to_do/', views.ToDoView.as_view(), name='to_do'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('ask/create/', views.AskCreateView.as_view(), name='ask_create'),
    path('ask/<int:pk>/update/', views.AskUpdateView.as_view(), name='ask_update'),


]