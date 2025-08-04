from django.urls import path
from downbeats.views.category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryDeleteView
from downbeats.views.subcategory import SubcategoryCreateView, SubcategoryDetailView, SubcategoryDeleteView
from downbeats.views.soundtrack import SoundtrackDetailView, SoundtrackCreateView, SoundtrackDeleteView

app_name = 'downbeats'

urlpatterns = [
    # Add your app's URL patterns here
    path("categories", CategoryListView.as_view(), name="categories"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("subcategory/<int:pk>/", SubcategoryDetailView.as_view(), name="subcategory_detail"),
    path("soundtrack/<int:pk>/", SoundtrackDetailView.as_view(), name="soundtrack_detail"),
    path("create_category", CategoryCreateView.as_view(), name="category_create"),
    path("create_subcategory", SubcategoryCreateView.as_view(), name="subcategory_create"),
    path("create_soundtrack", SoundtrackCreateView.as_view(), name="create_soundtrack"),
    path("delete_category/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("delete_subcategory/<int:pk>/", SubcategoryDeleteView.as_view(), name="subcategory_delete"),
    path("delete_soundtrack/<int:pk>/", SoundtrackDeleteView.as_view(), name="soundtrack_delete"),
]