from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models.query import Q

from core.models import Product, RentProduct
from api.serializers import ProductSerializer, MinProductSerializer
from eureka.utils import make_date


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
    permission_classes = [IsAuthenticated]
    serializer_class = MinProductSerializer

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Product.available_for_rents.filter(Q(name__icontains=q) | Q(code__icontains=q)) if q else Product.available_for_rents.all()
        return queryset


class CalculateEstimatedRent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        product_id = data.get('product_id')
        date_range = data.get('date_range')
        try:
            product = Product.available_for_rents.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'status': False, 'detail': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

        start, end = make_date(date_range)
        stat, detail = product.calculate_estimated_rent((end-start).days+1)
        return Response({'status': stat, 'detail': detail}, status=status.HTTP_200_OK)


class CalculateRentCost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = RentProduct.calculate_rent(request, api=True)
        message = 'Your rent fee: $%s. TOS violation fee: $%s. Total: $%s \nDo you want to proceed?' % (data['cost'], data['penalty'], data['penalty']+data['cost'])
        return Response({'status': True, 'cost': data['cost'], 'penalty': data['penalty'],
                         'message': message}, status=status.HTTP_200_OK)


class UserRentProductList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MinProductSerializer

    def get_queryset(self):
        return Product.objects.filter(rents__user=self.request.user, rents__return_date__isnull=True)
