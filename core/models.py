from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model
# class Device(models.Model):
#     title = models.CharField(max_length=200)
#     quantity = models.IntegerField(default = 0)
#     # moderation
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


#     def adding(self,request):
#         if request.method=='POST':
#             a = self.quantity
#             b = int(request.POST.get('number'))

#         c=a+b
#         print(c)
#         return c

category_choice = {
    ('Hub', 'Hub'),
    ('Switch', 'Switch'),
    ('Router', 'Router'),
    ('Access point', 'Access point'),
    ('Computer devices', 'Computer devices'),
    ('Electric devices', 'Electric devices'),
}


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name


class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                db_index=True, related_name='stocks', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    recieve_quantity = models.IntegerField(default=0, blank=True, null=True)
    recieve_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    receive_quantity = models.IntegerField(default=0, blank=True, null=True)

    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    # date = models.DateTimeField(auto_now_add=False, auto_now=False)

    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)

class StockHistory(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    recieve_quantity = models.IntegerField(default=0, blank=True, null=True)
    recieve_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    receive_quantity = models.IntegerField(default=0, blank=True, null=True)

    # user = models.CharField
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False,null=True)
    
    def __str__(self):
        return str(self.item_name)


# class Inventory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,
#                                db_index=True, related_name='inventories')
#     item_name = models.CharField(max_length=50, blank=True, null=True)
#     quantity = models.IntegerField(default=0, blank=True, null=True)
#     recieve_quantity = models.IntegerField(default=0, blank=True, null=True)
#     issue_quantity = models.IntegerField(default=0, blank=True, null=True)
#     description = models.CharField(max_length=100, blank=True, null=True)

#     last_updated = models.DateTimeField(auto_now_add=False, auto_now=True,null=True)
