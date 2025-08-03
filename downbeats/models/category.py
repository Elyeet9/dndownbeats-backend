from django.db import models
from dndownbeats.utils.models import BaseModel


class Category(BaseModel):
    """
    Model representing a category of items.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description", default="")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
    