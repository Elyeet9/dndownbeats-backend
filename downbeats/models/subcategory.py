from django.db import models
from dndownbeats.utils.models import BaseModel
from downbeats.models.category import Category


class Subcategory(BaseModel):
    """
    Model representing a subcategory of items.
    """

    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description", default="")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Category"
    )
    subcategory = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child_subcategories", blank=True, null=True, verbose_name="Parent Subcategory"
    )
    thumbnail = models.ImageField(
        upload_to="subcategories/thumbnails/",
        blank=True,
        null=True,
        verbose_name="Thumbnail"
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        ordering = ["name"]
        # Ensure unique names within the same category and parent subcategory
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category", "subcategory"],
                name="unique_subcategory_name_per_category_and_parent",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name}{' - ' + self.subcategory.name if self.subcategory else ''})"
