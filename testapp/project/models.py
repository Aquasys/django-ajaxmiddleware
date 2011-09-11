from django.db import models


class User(models.Model):
    """Basic model to test crud generic views"""

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
