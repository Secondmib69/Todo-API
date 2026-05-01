from django.shortcuts import render
from rest_framework import generics
from todo.models import Todo
from .serializers import TodoSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from .permissions import IsTodoUserOrStaffReadOnly, IsSuperUserOrStaffReadOnly
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
# Create your views here.

class RoleFilterBackend(DjangoFilterBackend): 
    def get_filterset_class(self, view, queryset=None):
        if not view.request.user.is_staff:
            return view.UserTodoFilter
        return view.StaffTodoFilter
    

class TodoListAPIView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    filter_backends = [SearchFilter, RoleFilterBackend, OrderingFilter]
    search_fields = ['title', 'body']
    # filterset_fields = ['user', 'is_done']
    ordering_fields = ['created', 'due_date', 'priority']
    ordering = ['priority']
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


    class StaffTodoFilter(FilterSet):
        class Meta:
            model = Todo
            fields = ['user', 'is_done']

    
    class UserTodoFilter(FilterSet):
        class Meta:
            model = Todo
            fields = ['is_done']



    def get_queryset(self):
        qs = Todo.objects.all()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs

    
    def perform_create(self, serializer): # create method in serializer can also be modified
        serializer.save(user=self.request.user)



class TodoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    lookup_url_kwarg = 'id'
    permission_classes = [IsTodoUserOrStaffReadOnly]
    authentication_classes = [JWTCookieAuthentication]


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrStaffReadOnly]
    authentication_classes =[JWTCookieAuthentication]
    pagination_class = LimitOffsetPagination