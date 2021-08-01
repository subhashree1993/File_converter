from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=70)
    email=models.EmailField(max_length=100, unique=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FileConvert(models.Model):
    # requestId=models.IntegerField()
    userId=models.IntegerField()
    fileName=models.CharField(max_length=100)
    originalFilePath=models.CharField(max_length=500)
    convertedFilePath=models.CharField(max_length=500)
    convertedFrom=models.CharField(max_length=20)
    convertedTo=models.CharField(max_length=20)
    requestedTime=models.DateTimeField()
    conversionStatus=models.BooleanField()

    def __str__(self):
        return self.id