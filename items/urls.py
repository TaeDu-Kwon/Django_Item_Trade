from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('game/',views.CreateGameView.as_view()),
    path('create/', views.CreateProductView.as_view(), name='create_product'),
    path('get-recently-create-item/',views.ProductViewsets.as_view({
        "get":"get_recently_create_item",
    })),
    path("get-product-info/<str:product_type>/<int:product_id>/",views.ProductViewsets.as_view({
        "get" : "get_product_info"
    })),
    path("buy-product/",views.ProductViewsets.as_view({
        "post" : "buy_the_product"
    }),name='buy_the_product'),
    path("purchase-record/",views.PurchaseRecordViewset.as_view({'get': 'list'}), name='purchase_record'),
    path('purchases/<int:pk>/', views.PurchaseRecordViewset.as_view({'get': 'list'}), name='purchase-detail'),
]




