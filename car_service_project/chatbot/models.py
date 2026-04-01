

# Create your models here.
# chatbot/models.py
from django.db import models

class CarService(models.Model):
    name = models.CharField(max_length=100) # e.g., "Engine Tuning"
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"
