from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'todo'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('todos/', TodoListAPIView.as_view(), name='todo-list'),
    path('todos/<int:id>/', TodoDetailAPIView.as_view(), name='todo-detail'),
]