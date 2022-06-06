from django.db import models
from eureka.g_model import BaseModel

PLAIN = 'plain'
METER = 'meter'

TypeChoice = (
    (PLAIN, 'plain'),
    (METER, 'meter')
)


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
    minimum_rent_period = models.PositiveIntegerField()
