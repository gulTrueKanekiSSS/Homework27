
from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show),
    path('saveads/', views.csv_to_json),
    path('savecat/', views.csv_cat_to_json),
    path('advertise/', views.AdvertismentView.as_view()),
    path('advertise/<int:pk>/', views.DetViewAds.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>/', views.DetViewCat.as_view())
]
