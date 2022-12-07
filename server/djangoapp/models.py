from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=80)
    description = models.CharField(max_length=300)

    def __str__(self):
        return "Make: " + self.name


class CarModel(models.Model):
    name = models.CharField(null=False, max_length=80)
    dealer_id = models.IntegerField()
   
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=CAR_TYPES,
        default=SEDAN
    )
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField()

    def __str__(self):
        return "Model: " + self.name


class CarDealer:

    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.state = state
        # Location st
        self.st = st
        # Location address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Dealer lat
        self.lat = lat
        # Dealer long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer full name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
