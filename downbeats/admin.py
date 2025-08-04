from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from downbeats.models.category import Category
from downbeats.models.subcategory import Subcategory
from downbeats.models.soundtrack import Soundtrack


class InlineSubcategory(admin.TabularInline):
    model = Subcategory
    extra = 1
    verbose_name = "Subcategory"
    verbose_name_plural = "Subcategories"
    readonly_fields = ('edit_link',)
    
    def edit_link(self, obj):
        if obj.pk:
            url = reverse('admin:downbeats_subcategory_change', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">Edit Subcategory</a>', url)
        return "Save to edit"
    
    edit_link.short_description = "Edit"


class InlineSoundtrack(admin.TabularInline):
    model = Soundtrack
    extra = 1
    verbose_name = "Soundtrack"
    verbose_name_plural = "Soundtracks"
    readonly_fields = ('edit_link',)
    
    def edit_link(self, obj):
        if obj.pk:
            url = reverse('admin:downbeats_soundtrack_change', args=[obj.pk])
            return format_html('<a href="{}" target="_blank">Edit Soundtrack</a>', url)
        return "Save to edit"
    
    edit_link.short_description = "Edit"


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [InlineSubcategory, InlineSoundtrack]


class CustomSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "subcategory")
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("category", "subcategory")
    inlines = [InlineSubcategory, InlineSoundtrack]


admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Subcategory, CustomSubcategoryAdmin)
admin.site.register(Soundtrack)