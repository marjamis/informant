from django.urls import include, path
from django.contrib import admin

app_name = "informant"
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('cloudtrail.urls', namespace="cloudtrail"))
]
