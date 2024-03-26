from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.title}"
