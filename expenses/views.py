import json
import datetime
import csv
import xlwt
import tempfile


from weasyprint import HTML


from django.core import paginator
from django.core.checks import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render 
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, response
from django.template.loader import render_to_string
from django.db.models import Sum


from userpreferences.models import UserPreferences

from .models import Expense, Category


def search_expense(request):
    if request.method == 'POST':
        serach_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith = serach_str, owner=request.user) | Expense.objects.filter(
            date__istartswith = serach_str, owner=request.user) | Expense.objects.filter(
            category__icontains = serach_str, owner=request.user) | Expense.objects.filter(
            description__icontains = serach_str, owner=request.user) 

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user = request.user).currency
    context = {
        "expenses": expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, "expenses/index.html", context)

def add_expenses(request):
    categories = Category.objects.all()

    context = {
        "categories" : categories,
        "values" : request.POST
    }

    if request.method == 'GET':
        
        return render(request, "expenses/add_expenses.html", context)

    if request.method == 'POST':

        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, "expenses/add_expenses.html", context)

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, "expenses/add_expenses.html", context)
        
        Expense.objects.create(owner= request.user, amount=amount, description=description,
                                date=date, category=category)
        messages.success(request, "Expense saved successfully")

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    
    context={
        "expense": expense,
        "values": expense,
        "categories" : categories
    }

    if request.method == 'GET':
        return render(request, "expenses/edit_expense.html", context)

    if request.method == 'POST':
        amount = request.POST['amount']
        
        if not amount:
            messages.error(request, 'Amount is required!')
            return render(request, "expenses/edit_expense.html", context)

        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required!')
            return render(request, "expenses/edit_expense.html", context)
        

        expense.owner= request.user
        expense.amount=amount
        expense.description=description
        expense.date=date
        expense.category=category

        expense.save()
        messages.success(request, "Expense Updated successfully")

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense Removed!")        
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte=todays_date)

    finalrep={}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        print("filtered_by_category", filtered_by_category)

        for item in filtered_by_category:
            amount += item.amount
            print("amount___", amount)
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)
    
    print('finalrep', finalrep)
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+\
        str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses= Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, 
                        expense.category, expense.date])
    
    return response


def export_excel(request):
    
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Expenses'+\
        str(datetime.datetime.now())+'.xlsx'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        
    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'description', 'category', 'date')
    
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

def export_pdf(request):
    # return render(request, "expenses/pdf_output.html")
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses'+\
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses  =Expense.objects.filter(owner=request.user)
    print("=========")
    sum = expenses.aggregate(Sum('amount'))

    html_string =  render_to_string(
        'expenses/pdf_output.html', {'expenses': expenses, 'total': sum['amount__sum']}
    )
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    print("after HTML ====")
    result = html.write_pdf()
    print("after result++")

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output= open(output.name, 'rb')
        response.write(output.read())
    print("after output")
    return response