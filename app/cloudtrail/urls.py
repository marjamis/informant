from django.conf.urls import url
from cloudtrail import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^results/', views.results, name='results'),
  url(r'^full_results/', views.full_results, name='full_results'),
  url(r'^raw_data/', views.raw_data, name='raw_data'),
]
