from django.urls import path
from cloudtrail import views

app_name = "cloudtrail"

urlpatterns = [
  path(r'', views.index, name='index'),
  path(r'results/', views.results, name='results'),
  path(r'full_results/', views.full_results, name='full_results'),
  path(r'raw_data/', views.raw_data, name='raw_data'),
]
