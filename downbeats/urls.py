from django.urls import path
from downbeats.views.category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryDeleteView
from downbeats.views.subcategory import SubcategoryCreateView, SubcategoryDetailView
from downbeats.views.soundtrack import SoundtrackCreateView

app_name = 'downbeats'

urlpatterns = [
    # Add your app's URL patterns here
    path("categories", CategoryListView.as_view(), name="categories"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("subcategory/<int:pk>/", SubcategoryDetailView.as_view(), name="subcategory_detail"),
    path("create_category", CategoryCreateView.as_view(), name="category_create"),
    path("create_subcategory", SubcategoryCreateView.as_view(), name="subcategory_create"),
    path("create_soundtrack", SoundtrackCreateView.as_view(), name="create_soundtrack"),
    path("delete_category/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
]