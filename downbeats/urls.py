from django.urls import path
from downbeats.views.category import CategoryListView, CategoryDetailView

app_name = 'downbeats'

urlpatterns = [
    # Add your app's URL patterns here
    path("categories", CategoryListView.as_view(), name="categories"),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
]