from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class User(models.Model):
#     username = models.CharField(max_length=128)
#     password = models.CharField(max_length=128)
#     email = models.CharField(max_length=128)
#
#     def __str__(self):
#         return "pk {}) {} {}".format(self.id, self.username, self.email)


class Image(models.Model):
    name = models.CharField(max_length=128)
    path = models.FileField(upload_to='documents/')
    ascii = models.CharField(max_length=10000)
    creator = models.ForeignKey(User, related_name="img_creator")

    def __str__(self):
        return "pk {}) {} - {}".format(self.id, self.name, self.path)


