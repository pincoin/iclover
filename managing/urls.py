from django.urls import path
from  django.contrib.auth import views as auth_views
from . import views

app_name = 'managing'

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.change_password, name='change_password'),
    path('', views.Main.as_view(), name='main'),

    path('customer_profile/', views.CustomerWriteProfileView.as_view(), name='customer_profile'),
    path('customer_profile/create/', views.CustomerProfileView.as_view(), name='customer_profile_create'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),

    path('memo/create/<slug:common>/', views.MemoCreateView.as_view(), name='memo_create'),
    path('memo/<int:pk>/update/', views.MemoUpdateView.as_view(), name='memo_update'),
    path('customer_result/', views.CustomerResultView.as_view(), name='customer_result'),

    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('order_view/', views.OrderView.as_view(), name='order_view'),
    path('order_view/create/', views.OrderCreateAPIView.as_view(), name='order_view_create'),


    path('product/', views.ProductView.as_view(), name='product'),
    path('product/create/', views.ProdcutCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('special_price/', views.SpecialPriceView.as_view(), name='special_price'),
    path('special_price/create/', views.SpecialPriceCreateView.as_view(), name='special_price_create'),
    path('special_price/<int:pk>/update/', views.SpecialPriceUpdateView.as_view(), name='special_price_update'),
    path('special_price/<int:pk>/delete/', views.SpecialPriceDeleteView.as_view(), name='special_price_delete'),
    path('sample/', views.SampleView.as_view(), name='sample'),
    path('sample/create/', views.SampleCreateView.as_view(), name='sample_create'),
    path('sample/<int:pk>/update/', views.SampleUpdateView.as_view(), name='sample_update'),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:kind>_<int:level>/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:kind>_<int:level>_<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('discount/', views.DiscountView.as_view(), name='discount'),
    path('img_box/', views.ImageBoxView.as_view(), name='img_box'),
    path('order/<int:common>/', views.OrderListView.as_view(), name='order'),
    path('orders/create/', views.OrdersCreateView.as_view(), name='orders_create'),
    path('orders/<int:pk>/update/', views.OrdersUpdateView.as_view(), name='order_update'),
    path('demand_list/', views.DemandView.as_view(), name='demand_list'),
    path('employees/', views.EmployeesView.as_view(), name='employees'),
    path('employees/create/', views.EmployeesCreateView.as_view(), name='employees_create'),
    path('employees/<int:pk>/update/', views.EmployeesUpdateView.as_view(), name='employees_update'),
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('deposit/create/', views.DepositCreateView.as_view(), name='deposit_create'),
    path('deposit/<int:pk>/update/', views.DepositUpdateView.as_view(), name='deposit_update'),
    path('deposit/<int:pk>/delete/', views.DepositDeleteView.as_view(), name='deposit_delete'),
    path('order_deposit/<int:pk>/', views.OrderWithDepositCreateView.as_view(), name='order_deposit'),
    path('order_images/<int:pk>/', views.OrderWithImagesCreateView.as_view(), name='order_images'),
    path('order_images/<int:pk>/delete/', views.OrderWithImagesDeleteView.as_view(), name='order_images_delete'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('bill/<int:pk>/', views.BillView.as_view(), name='bill'),
    path('my_page/', views.MyPageView.as_view(), name='my_page'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('ask/create/', views.AskCreateView.as_view(), name='ask_create'),
    path('ask/<int:pk>/update/', views.AskUpdateView.as_view(), name='ask_update'),


]