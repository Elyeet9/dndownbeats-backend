from django.db import models
from dndownbeats.utils.models import BaseModel
from dndownbeats.utils.constants import SOUNDTRACK_ORIGIN_CHOICES
from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory


class Soundtrack(BaseModel):
    """
    Model representing a soundtrack.
    """

    title = models.CharField(blank=False, null=False, max_length=200, verbose_name="Soundtrack Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description", default="")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="soundtracks", 
        blank=False,
        null=False,
        verbose_name="Category"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="soundtracks",
        blank=True,
        null=True,
        verbose_name="Subcategory"
    )
    origin = models.CharField(
        choices=SOUNDTRACK_ORIGIN_CHOICES,
        max_length=50,
        default=SOUNDTRACK_ORIGIN_CHOICES[0][0],
        verbose_name="Origin"
    )
    url = models.URLField(blank=False, null=False, verbose_name="Soundtrack URL")
    thumbnail = models.ImageField(
        upload_to="soundtracks/thumbnails/",
        blank=True,
        null=True,
        verbose_name="Thumbnail"
    )

    class Meta:
        verbose_name = "Soundtrack"
        verbose_name_plural = "Soundtracks"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}"