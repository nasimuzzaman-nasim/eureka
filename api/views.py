from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from core.models import Product
from api.serializers import ProductSerializer


class CreateSingleProduct(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreateMultipleProduct(CreateSingleProduct):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)