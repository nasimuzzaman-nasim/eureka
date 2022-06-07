from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView

from core.models import Product


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'product_list.html'
    paginate_by = 5
    model = Product
    
    def get_context_data(self, *args, **kwargs):
        data = super(ProductListView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Products'
        data['base_count'] = (int(self.request.GET.get('page', 1)) - 1) * self.paginate_by

        return data
        
