from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    addition_date = models.DateTimeField(auto_now_add=True, null=True)
    prep_time = models.IntegerField(null=True, blank=True)
    cooking_time = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True)


    def total_time(self):
        prep = self.prep_time if self.prep_time is not None else 0
        cook = self.cooking_time if self.cooking_time is not None else 0
        return prep + cook


    def __str__(self):
        return self.title