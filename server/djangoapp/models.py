from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=True, max_length=500)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    VEHICLE_TYPE_CHOICES = [
            ("sedan","Sedan"),
            ("coupe","Coupe"),
            ("sports","Sports"),
            ("hatchback","Hatchback"),
            ("van","Van"),
            ("suv","SUV"),
            ("truck","Truck")
    ]
    name = models.CharField(max_length=30,blank=False)
    dealerId = models.IntegerField(blank=False)
    type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default="sedan")
    year = models.DateField(null=True)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return "Car Make: " + self.carmake.name + "," + \
               "Description: " + self.carmake.description + "," + \
               "Car Model: " + self.name + "," + \
               "Dealer ID: " + str(self.dealerId) + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
