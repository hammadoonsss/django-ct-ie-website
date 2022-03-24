from django.contrib import admin
from .models import UserIncome, Source
# Register your models here.

class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', "description", "owner", "source", "date",)
    search_fields = ("description", "source", "date",)

    list_per_page = 5


admin.site.register(UserIncome, UserIncomeAdmin)
admin.site.register(Source)
