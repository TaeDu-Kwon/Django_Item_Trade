from django.urls import path

from . import views

app_name = "item_trade"

urlpatterns = [
    path("",views.home_page, name = "home_page"),
    path("logout/",views.logout_view, name = "logout"),
    path("login-page/",views.login_page, name = "login_page"),
    path("signup-page/",views.signup_page, name = "signup_page"),
    path('create-product/', views.create_product_view, name='create_product'),
]

