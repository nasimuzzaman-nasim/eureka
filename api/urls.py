from rest_framework.urls import path
from api.views import CreateMultipleProduct, CreateSingleProduct

urlpatterns = [
    path('create-single-product', CreateSingleProduct.as_view(), name='create_single_product_api'),
    path('create-multiple-product', CreateMultipleProduct.as_view(), name='create_multiple_product_api'),
]