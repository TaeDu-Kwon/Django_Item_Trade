from django.urls import path

from . import views

app_name = "item_trade"

urlpatterns = [
    path("",views.home_page, name = "home_page"),
    path("logout/",views.logout_view, name = "logout"),
    path("login-page/",views.login_page, name = "login_page"),
    path("signup-page/",views.signup_page, name = "signup_page"),
    path("buy-credit/<int:user_id>",views.credit_page, name = "credit_page"),
    path('create-product/', views.create_product_view, name='create_product'),
    path('product-info/<str:product_type>/<int:product_id>', views.product_info_page, name = "product_info"),
    path('product-purchase/<str:product_type>/<int:product_id>',views.product_purchase_page, name = "product_purchase"),
    path('buy-the-product',views.buy_the_product, name = "buy_the_product"),
    path('payment-fail',views.payment_fail, name = "payment_fail"),
    path("kakaopay/<str:user_name>", views.kakaopay, name = "kakaopay"),
    path('paySuccess/', views.paySuccess),
    path('payFail/', views.payFail),
    path('payCancel/', views.payCancel),
]

