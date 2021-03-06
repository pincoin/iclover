from django.urls import include, path
from rest_framework import routers
from django.conf import settings

from . import views

app_name = 'rowapi'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'profile', views.ProfileViewSet)
router.register(r'customer_profile', views.CustomerProfileViewSet)
router.register(r'product_view', views.ProductViewSet)
# router.register(r'product', views.ProductTextViewSet)
router.register(r'order_info', views.OrderInfoViewSet, base_name='order_info')
router.register(r'cart_design', views.CartDesignViewSet, base_name='cart_design')
# router.register(r'user_profile', views,ProfileViewSet)

urlpatterns = router.urls
# if settings.DEBUG:
#     urlpatterns += [
#         path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#     ]