from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models.query import Q

from core.models import Product


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'product_list.html'
    paginate_by = 15
    model = Product

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super(ProductListView, self).get_queryset()
        return queryset.filter(Q(name__icontains=q) | Q(code__icontains=q)) if q else queryset

    def get_context_data(self, *args, **kwargs):
        data = super(ProductListView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Products'
        data['base_count'] = (int(self.request.GET.get('page', 1)) - 1) * self.paginate_by

        return data
        
