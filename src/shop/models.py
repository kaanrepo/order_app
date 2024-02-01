from django.db import models
from django.utils.text import slugify
import random
import string

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
    handle = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='product', blank=True, null=True)
    image2 = models.ImageField(upload_to='product', blank=True, null=True)

    class Meta:
        unique_together = ('name', 'unit', 'size',)

    def __str__(self):
        return self.name + ' ' + self.size + ' ' + self.unit
    
    def save(self, *args, **kwargs):
        if not self.handle:
            slug_string = '-'.join([self.name, self.size, self.unit])
            self.handle = slugify(slug_string)
        super().save(*args, **kwargs)

class MenuCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    handle = models.SlugField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = slugify(self.name)
        super().save(*args, **kwargs)
    
class MenuItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    handle = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.name + ' ' + self.product.size + ' ' + self.product.unit + ' ' + str(self.price)
    
    def save(self, *args, **kwargs):
        if not self.handle:
            slug_string = '-'.join([self.product.name, self.product.size, self.product.unit])
            self.handle = slugify(slug_string)
        super().save(*args, **kwargs)
    
class Table(models.Model):
    name = models.CharField(max_length=50, unique=True)
    in_use = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    handle = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = slugify(self.name)
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.menu_item.product.name + 'x' + str(self.quantity)
    
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