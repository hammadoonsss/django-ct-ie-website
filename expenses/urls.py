from django.urls import path
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from expenses import views

urlpatterns = [
    path("", views.index, name="expenses"),
    path("add_expenses", views.add_expenses, name="add_expenses"),
    path("edit_expense/<int:id>", views.edit_expense, name="edit_expense"),
    path("delete_expense/<int:id>", views.delete_expense, name="delete_expense"),
    path("search-expenses", csrf_exempt(views.search_expense), name="search-expenses"),

    path('expense_category_summary', views.expense_category_summary, name="expense_category_summary"),

    path('stats', views.stats_view, name="stats"),
    path('export_csv', views.export_csv, name="export_csv"),
    path('export_excel', views.export_excel, name="export_excel"),
    path('export_pdf', views.export_pdf, name="export_pdf"),


]