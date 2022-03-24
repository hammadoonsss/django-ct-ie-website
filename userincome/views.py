import json
from django.contrib.auth.models import User

from django.core import paginator
from django.core.checks import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render 
from django.core.paginator import Paginator
from django.http import JsonResponse

from userpreferences.models import UserPreferences

from .models import Source, UserIncome

def search_income(request):
    if request.method == 'POST':
        serach_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith = serach_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith = serach_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains = serach_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains = serach_str, owner=request.user) 

        data = income.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)

    paginator = Paginator(income, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user = request.user).currency
    context = {
        "income": income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, "income/index.html", context)

def add_income(request):
    sources = Source.objects.all()

    context = {
        "sources" : sources,
        "values" : request.POST
    }

    if request.method == 'GET':
        
        return render(request, "income/add_income.html", context)

    if request.method == 'POST':

        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, "income/add_income.html", context)

        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, "income/add_income.html", context)
        
        UserIncome.objects.create(owner= request.user, amount=amount, description=description,
                                date=date, source=source)
        messages.success(request, "Income Record saved successfully")

        return redirect('income')


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    
    context={
        "income": income,
        "values": income,
        "sources" : sources
    }

    if request.method == 'GET':
        return render(request, "income/edit_income.html", context)

    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, "income/edit_income.html", context)

        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, "income/edit_income.html", context)
        

        income.owner= request.user
        income.amount=amount
        income.description=description
        income.date=date
        income.source=source

        income.save()
        messages.success(request, "Income Updated successfully")

        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income Removed!")        
    return redirect('income')
