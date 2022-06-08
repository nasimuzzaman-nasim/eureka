from django.urls import path

from core.views import DashboardView, ProductListView, RentProductView

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard_url'),
    path('products/', ProductListView.as_view(), name='product_list_url'),
    path('rent-product/', RentProductView.as_view(), name='rent_product_url'),
]