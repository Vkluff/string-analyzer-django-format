from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from analyzer.views import StringViewSet

router = DefaultRouter()
router.register(r'strings', StringViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]
