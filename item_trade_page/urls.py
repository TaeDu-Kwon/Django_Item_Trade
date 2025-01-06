from django.urls import path

from . import views

app_name = "item_trade"

urlpatterns = [
    path("home_page/",views.home_page, name = "home_page"),
    path("login_page/",views.login_page, name = "login_page"),
    path("signup_page/",views.signup_page, name = "signup_page"),
    path('create-product/', views.create_product_view, name='create_product'),
]

