from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = [
            'created_at',
            'updated_at'
        ]

    # def to_representation(self, instance):
    #     data = super(ProductSerializer, self).to_representation(instance)
    #     data['type'] = instance.get_type_display()
    #     return data