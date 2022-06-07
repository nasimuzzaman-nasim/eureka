from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.query import Q

from core.models import Product
from api.serializers import ProductSerializer


class CreateSingleProduct(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreateMultipleProduct(CreateSingleProduct):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(availability=True, needing_repair=False)

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super(ProductList, self).get_queryset().filter(availability=True, needing_repair=False)
        return queryset.filter(Q(name__icontains=q) | Q(code__icontains=q)) if q else queryset