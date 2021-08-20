from . import views
from .views import *
from .forms import UserLoginForm
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('registration/', views.CaUserSignUpView.as_view(), name="user_register"),
    path('admin_registration/', views.AdminSignUpView.as_view(), name="admin_register"),
    path('products/', views.products, name="products"),
    path('products/<category_name>', views.products, name="products_by_category"),
    path('product/<int:product_id>', views.product, name="product"),
    path('productform/', views.product_form),
    path('basket/', views.basket, name="basket"),
    path('addbasket/<int:product_id>', views.add_to_basket, name="add_to_basket"),
    path('addfrombasket/<int:product_id>', views.add_from_basket, name="add_from_basket"),
    path('removebasket/<int:product_id>', views.remove_from_basket, name="remove_from_basket"),
    path('orderform/', views.order_form),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-registration/', UserViewSet.as_view({'get': 'list'}), name="api_user_register"),
    path('token/', obtain_auth_token, name="api_token_auth")
]

