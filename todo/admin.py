from django.contrib import admin
from todo.models import Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created', 'priority', 'is_done']
    list_editable = ['is_done']
