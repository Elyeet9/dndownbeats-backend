from django.urls import path
from downbeats.views.category import CategoryListView, CategoryDetailView, CategoryCreateView
from downbeats.views.subcategory import SubcategoryDetailView

app_name = 'downbeats'

urlpatterns = [
    # Add your app's URL patterns here
    path("categories", CategoryListView.as_view(), name="categories"),
    path("category_create", CategoryCreateView.as_view(), name="category_create"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("subcategory/<int:pk>/", SubcategoryDetailView.as_view(), name="subcategory_detail"),
]