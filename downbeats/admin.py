from django.contrib import admin

# Register your models here.
from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory
from downbeats.models.soundtrack import Soundtrack


class InlineSubcategory(admin.TabularInline):
    model = Subcategory
    extra = 1
    verbose_name = "Subcategory"
    verbose_name_plural = "Subcategories"


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [InlineSubcategory]


admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Soundtrack)