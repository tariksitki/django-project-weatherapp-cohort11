from django.db import models

# Create your models here.


    ### user in search ile girdigi sehir ismi var ise db ye kaydedecegiz:
class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 