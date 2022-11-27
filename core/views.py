from django.shortcuts import render,redirect
from core.models import Stock,StockHistory
from core.forms import StockCreateForm,StockSearchForm,StockUpdateForm,IssueForm,ReceiveForm,ReorderLevelForm,HistoryStockCreateForm,HistoryIssueForm,HistoryReceiveForm
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login

def index(request):
    device = Stock.objects.all()

    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request,'index.html',{'devices': device,'form':form})

@login_required
def list_items(request):
    title = 'List of list_items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'form'  : form,
        'title' : title,
        'queryset' : queryset,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value())

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME','QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category,stock.item_name,stock.quantity])
            return response

        context = {
        'form'  : form,
        'title' : title,
        'queryset' : queryset,
    }
    
    return render(request, 'list_items.html',context)





@login_required
def update_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('/list_items')
    context = {
        'form': form,
        'title': "Add Item"
    }
    return render(request, 'add_items.html', context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    form1 = HistoryStockCreateForm(request.POST or None)
    if form.is_valid() and form1.is_valid:
        form.save()
        form1.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        'form' : form,
        'form': form1,
        'title' : 'Add item'
    }
    return render(request,'add_items.html',context)

@login_required
def delete_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    queryset1 = StockHistory.objects.filter(item_name=queryset.item_name,category=queryset.category)

    if request.method == 'POST':
        queryset.delete()
        queryset1.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_items')
    return render(request,'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        'title': queryset.item_name,
        'queryset': queryset,
    }
    return render(request,'stock_detail.html',context)


def issue_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance = queryset)
    form1 = HistoryIssueForm(request.POST or None)
    
    if form.is_valid() and form1.is_valid:
        # form1.instance = form.instance 
        form1.instance.item_name = form.instance.item_name
        form1.instance.category = form.instance.category
        instance = form.save(commit=False)
        # instance1 = form1.save(commit=False)
        form1.save()
        # instance.receive_quantity = 0
        instance.quantity = instance.quantity - instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")
        instance.save()
        # instance1.save()
        print('aaaaaaaaa',instance)
        # print('bbbbbbbbb',instance1)
        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form' : form,
        'form' : form1, 
        'username': 'Issue By: ' + str(request.user),
    }

    return render(request,'add_items.html',context)

def receive_items(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance = queryset)
    form1 = HistoryReceiveForm(request.POST or None)
    
    if form.is_valid() and form1.is_valid:
        instance = form.save(commit=False)
        form1.instance.item_name = form.instance.item_name
        form1.instance.category = form.instance.category
        form1.save()
        # instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/stock_detail/'+str(instance.id))
    
    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form' : form,
        'form' : form1, 
        'username': 'Issue By: ' + str(request.user),
    }

    return render(request,'add_items.html',context)
    

def reorder_level(request,pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None,instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Reorder level for ' + str(instance.item_name) + ' is updated to ' + str(instance.reorder_level))
        return redirect ('/list_items')

    context = {
        'instance': queryset,
        'form': form,
    }
    return render(request, "add_items.html",context)


@login_required
def list_history(request):
    header = 'LIST OF HISTORY'
    queryset = StockHistory.objects.all()
    # for i in queryset:
    #     for j in i:
    #         print(j)
    context = {
        'header': header,
        'queryset': queryset,
    }

    return render(request,'list_history.html',context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is None:
            context = {'error': 'Invalid username or password'}
            return render(request,'login.html',context)
        login(request,user)
        return redirect('/list_items')
    return render(request,'login.html')

def logout_view(request):
    return render(request,'login.html')


@login_required
def logs(request):
    title = 'List of list_items'
    
    queryset = Stock.objects.all()
    

    context = {
        
        'title' : title,
        'queryset' : queryset,
    }
    
    return render(request, 'logs.html',context)