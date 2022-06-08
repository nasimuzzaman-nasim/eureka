from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from api.views import (CreateMultipleProduct, CreateSingleProduct,
                       ProductList, CalculateEstimatedRent)

app_name = 'api'

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair_api'),
    path('create-single-product', CreateSingleProduct.as_view(), name='create_single_product_api'),
    path('create-multiple-product', CreateMultipleProduct.as_view(), name='create_multiple_product_api'),
    path('products', ProductList.as_view(), name='products_api'),
    path('calculate-estimated-rent', CalculateEstimatedRent.as_view(), name='calculate_estimated_rent_api'),
]