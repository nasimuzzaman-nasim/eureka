from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from django.db.models.query import Q
from django.conf import settings

from core.models import Product, RentProduct
from eureka.utils import return_book_operation


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        data = super(DashboardView, self).get_context_data(**kwargs)
        data['title'] = 'Dashboard'
        data['total'] = Product.objects.count()
        data['available'] = Product.available_for_rents.count()
        data['rent'] = RentProduct.objects.filter(return_date__isnull=True).count()
        data['repair'] = Product.objects.filter(needing_repair=True).count()

        return data


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'product_list.html'
    paginate_by = settings.PER_PAGE
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


class RentProductView(LoginRequiredMixin, View):
    def post(self, request):
        status, obj = RentProduct.create_rent(request)
        return JsonResponse({'status': status, 'detail': None if status else obj}, safe=False)


class ReturnProductView(LoginRequiredMixin, View):
    def post(self, request):
        data = RentProduct.calculate_rent(request)
        return_book_operation(data)
        return JsonResponse({'status': True}, status=200)


class RentProductList(LoginRequiredMixin, ListView):
    template_name = 'rent_list.html'
    paginate_by = settings.PER_PAGE
    model = RentProduct

    def get_context_data(self, *args, **kwargs):
        data = super(RentProductList, self).get_context_data(*args, **kwargs)
        data['title'] = 'Rent'
        data['base_count'] = (int(self.request.GET.get('page', 1)) - 1) * self.paginate_by

        return data
