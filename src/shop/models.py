from django.db import models
from django.utils.text import slugify
import random
import string
from django.db.models import Q

UNIT_CHOICES = [
    ('draft', 'Draft'),
    ('bottle', 'Bottle'),
    ('can', 'Can'),
    ('glass', 'Glass'),
    ('bowl', 'Bowl'),
    ('plate', 'Plate'),
]


class ProductManager(models.Manager):
    """Manager for Product model."""

    def search(self, query):
        """Search for product."""
        return self.filter(
            Q(name__icontains=query) |
            Q(size__icontains=query) |
            Q(unit__icontains=query)
        ).distinct()

class Product(models.Model):
    """Model for product in the shop."""

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(
        max_length=50, choices=UNIT_CHOICES, default='draft')
    size = models.CharField(max_length=50)
    handle = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='product', blank=True, null=True)
    image2 = models.ImageField(upload_to='product', blank=True, null=True)

    objects = ProductManager()

    class Meta:
        """Meta definition for Product."""
        unique_together = ('name', 'unit', 'size',)

    def __str__(self):
        return self.name + ' ' + self.size + ' ' + self.unit

    def save(self, *args, **kwargs):
        if not self.handle:
            slug_string = '-'.join([self.name, self.size, self.unit])
            self.handle = slugify(slug_string)
        super().save(*args, **kwargs)

    def get_prefix(self):
        return f"products/{self.id}/"


class MenuCategory(models.Model):
    """Model for menu category."""

    name = models.CharField(max_length=50, unique=True)
    handle = models.SlugField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.handle:
            self.handle = slugify(self.name)
        super().save(*args, **kwargs)

    def get_prefix(self):
        return f"category/{self.id}/"


class MenuItem(models.Model):
    """Model for menu item."""

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(
        MenuCategory, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    handle = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} {self.product.size} {self.product.unit} {self.price}"

    def save(self, *args, **kwargs):
        if not self.handle:
            slug_string = '-'.join([self.product.name,
                                   self.product.size, self.product.unit])
            self.handle = slugify(slug_string)
        super().save(*args, **kwargs)

class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"
    

class Table(models.Model):
    """Model for table in the restaurant."""
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    in_use = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    # handle = models.SlugField(null=True, blank=True)  DOES NOT NEED A HANDLE

    def __str__(self):
        return f"{self.name}"

    # def save(self, *args, **kwargs):
    #     if not self.handle:
    #         self.handle = slugify(self.name)
    #     super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Model for order item."""

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.menu_item.product.name} x {self.quantity}"


class OrderQuerySet(models.QuerySet):
    def search(self, query):
        """Search for order."""
        return self.filter(
            Q(id__icontains=query) |
            Q(table__name__icontains=query)|
            Q(created__icontains=query)
        ).distinct()


class OrderManager(models.Manager):
    """Manager for Order model."""
    def get_queryset(self):
        """Search for order."""
        return OrderQuerySet(self.model, using=self._db)


class Order(models.Model):
    """Model for order."""

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    objects = OrderManager()

    @property
    def total_bill(self):
        """ Calculate total bill for the order."""
        return sum([item.menu_item.price * item.quantity for item in self.orderitem_set.all() if item.is_delivered])

    def __str__(self):
        return self.table.name + '- order:' + str(self.id)
