from django.db import models


UNIT_CHOICES = [
    ('draft', 'Draft'),
    ('bottle', 'Bottle'),
    ('can', 'Can'),
    ('glass', 'Glass'),
    ('bowl', 'Bowl'),
    ('plate', 'Plate'),
        ]

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES ,default='draft')
    size = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product', blank=True, null=True)
    image2 = models.ImageField(upload_to='product', blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.size + ' ' + self.unit
    
class MenuCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name + ' ' + self.product.size + ' ' + self.product.unit + ' ' + str(self.price)
    
class Table(models.Model):
    name = models.CharField(max_length=50)
    in_use = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product.name + 'x' + str(self.quantity)
    
class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    @property
    def total_bill(self):
        return sum([item.product.price * item.quantity for item in self.orderitem_set.all() if item.is_delivered])
    
    def __str__(self):
        return self.table.name + '- order:' +str(self.id)