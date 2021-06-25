from django.contrib import admin
from .models import Users, Complex, Procedures


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'status', 'subscribe', 'black_list')
    list_filter = ('username', 'black_list')


@admin.register(Complex)
class ComplexAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ('title',)


@admin.register(Procedures)
class ProceduresAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ('title',)

