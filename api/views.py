from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.query import Q

from core.models import Product
from api.serializers import ProductSerializer, MinProductSerializer
from eureka.utils import split_date


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
    serializer_class = MinProductSerializer
    queryset = Product.objects.filter(availability=True, needing_repair=False)

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = super(ProductList, self).get_queryset().filter(availability=True, needing_repair=False)
        return queryset.filter(Q(name__icontains=q) | Q(code__icontains=q)) if q else queryset


class CalculateEstimatedRent(APIView):
    def post(self, request):
        data = request.data
        product_id = data.get('product_id')
        date_range = data.get('date_range')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'status': False, 'detail': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

        start, end = split_date(date_range)
        stat, detail = product.calculate_estimated_rent((end-start).days+1)
        return Response({'status': stat, 'detail': detail}, status=status.HTTP_200_OK)