from django import forms
from .models import Table, Order, OrderItem, Product, MenuItem, MenuCategory
from django.urls import reverse

class InactiveTableForm(forms.Form):
    table = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].choices = [(table.id, table.name) for table in Table.objects.filter(in_use=False)]


    def clean_table(self):
        table_id = self.cleaned_data['table']
        if False in [order.is_finished for order in Order.objects.filter(table__id=table_id)]:
            raise forms.ValidationError('Table is already in use')
        return table_id

class OrderPaidFinishedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_paid', 'is_finished']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class OrderItemForm(forms.Form):
#     product = forms.ChoiceField()
#     quantity = forms.IntegerField()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].choices = [(product.product.id, product.product) for product in MenuItem.objects.filter(is_active=True)]


class OrderItemForm(forms.Form):
    quantity=forms.IntegerField(min_value=1, initial=1)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image', 'image2']

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        exclude = ['is_active']