from django.db import models
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Case, Q, When
from datetime import date

from eureka.g_model import BaseModel
from eureka.utils import make_date

PLAIN = 'plain'
METER = 'meter'

TypeChoice = (
    (PLAIN, 'plain'),
    (METER, 'meter')
)


class AvailableProductManager(models.Manager):
    def get_queryset(self):
        """
            # durability should be less than max durability of that product
            # 10 miles will be taken every day.
            # mileage should be >=  minimum_rent_period * 10
        :return: a queryset of available product to rent
        """

        query = {
            'availability': True,
            'needing_repair': False,
            'durability__lt': F('max_durability'),

        }
        return super().get_queryset().filter(**query)\
            .filter(Q(mileage__gte=Case(When(type=METER, then=F('minimum_rent_period')*10))) | Q(mileage__isnull=True))


class Product(BaseModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=55)
    type = models.CharField(max_length=15, choices=TypeChoice)
    availability = models.BooleanField()
    needing_repair = models.BooleanField()
    durability = models.PositiveIntegerField()
    max_durability = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    minimum_rent_period = models.PositiveIntegerField()

    objects = models.Manager()
    available_for_rent = AvailableProductManager()

    def __str__(self):
        return '%s - %s' % (self.code, self.name)

    @property
    def full_name(self):
        return '%s - %s' % (self.code, self.name)

    @property
    def current_price(self):
        return self.discount_rate if self.discount_rate else self.price

    def calculate_estimated_rent(self, rent_period):
        d_loss = rent_period * 2 if self.type == METER else rent_period

        # 10 miles will be taken every day.
        if self.type == PLAIN or self.mileage - rent_period * 10:
            if self.durability + d_loss < self.max_durability:
                if self.minimum_rent_period <= rent_period:
                    estimated_fee = rent_period * self.current_price
                    return True, estimated_fee
                else:
                    return False, 'Minimum rent period is %s days!' % self.minimum_rent_period
            else:
                return False, 'Max durability exceed!'
        else:
            return False, 'Mileage error!'


class RentProduct(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rents')

    rent_start = models.DateField()
    rent_end = models.DateField()
    estimated_cost = models.DecimalField(max_digits=14, decimal_places=2)

    return_date = models.DateField(null=True)
    actual_cost = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    penalty = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    def __str__(self):
        return '%s -> %s' % (self.user.username, self.product)

    @classmethod
    def create_rent(cls, request):
        data = request.POST
        product_id = data.get('product_id')
        date_range = data.get('date_range')
        start, end = make_date(date_range)
        try:
            product = Product.available_for_rent.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404

        status, estimated_cost = product.calculate_estimated_rent((end-start).days+1)
        if not status:
            return status, estimated_cost

        rent = cls(
            product=product,
            user=request.user,
            estimated_cost=estimated_cost,
            rent_start=start,
            rent_end=end
        )
        rent.save()
        return True, rent

