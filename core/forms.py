from django import forms
from core.models import  Stock,StockHistory



# class DeviceForm(forms.ModelForm):
#     class Meta:
#         model = Device
#         fields = (
#             'title',
#             'quantity',
            
            
#         )

#         widgets = {
            
#             'title' : forms.TextInput(attrs={
#                                 'class': 'form-control',
#                                 'name': 'number'
#             }),
            
#         } 

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity'] 

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if not category:
    #         raise forms.ValidationError('This field is required')
        
    #     for instance in Stock.objects.all():
    #         if instance.category == category:
    #             raise forms.ValidationError(category + ' is already created')
    #     return category

    # def clean_item_name(self):
    #     item_name = self.cleaned_data.get('item_name')
    #     if not item_name:
    #         raise forms.ValidationError('This field is required')
    #     return item_name

class HistoryStockCreateForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'quantity'] 

    

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name','quantity']


class HistoryStockUpdateForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['category', 'item_name','quantity']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity','issue_to']

class HistoryIssueForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['issue_quantity','issue_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity','receive_by']

class HistoryReceiveForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['receive_quantity','receive_by']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

# class HistoryIssueForm(forms.ModelForm):
#     class Meta:
#         model = StockHistory
#         fields = 


