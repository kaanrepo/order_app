from django import forms
from .models import Table, Order, OrderItem, Product, MenuItem, MenuCategory, Section
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import InlineField
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
        exclude = ['image2', 'handle']
        help_texts = {
            'image': 'Enter the price of the product',
        }



    def clean_image(self):
        old_image = self.instance.image
        new_image = self.cleaned_data.get('image')
        if old_image and old_image != new_image:
            old_image.delete(save=False)
        return new_image
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.form
        self.helper.layout = Layout(
            HTML('<h1 class="text-center">Product Form</h1>'),
            *[Div(InlineField(field), css_class='col-md-6 offset-md-3 mb-3') for field in self.fields],
             HTML('<p class="text-center">Only images with size less than 2MB.</p>'),

        )

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        exclude= ['handle', 'product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['category'].empty_label = "Select a category"
        self.helper.form_show_labels = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h1 class="text-center">Menu Item Form</h1>'),
            *[Div(InlineField(field), css_class='col-md-6 offset-md-3 mb-3') for field in self.fields],
        )


class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = '__all__'
        exclude = ['handle']
    
    def clean_image(self):
        old_image = self.instance.image
        new_image = self.cleaned_data.get('image')
        if old_image and old_image != new_image:
            old_image.delete(save=False)
        return new_image
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h1 class="text-center">Category Form</h1>'),
            *[Div(InlineField(field), css_class='col-md-6 offset-md-3 mb-3') for field in self.fields],
            HTML('<p class="text-center">Only images with size less than 2MB.</p>'),
            Submit('submit', 'Save', css_class='btn btn-dark mt-3 mb-3 col-md-6 offset-md-3')
        )


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'
        exclude = ['in_use']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['section'].empty_label = "Select a section"
        self.helper.layout = Layout(
            HTML('<h1 class="text-center">Table Form</h1>'),
            *[Div(InlineField(field), css_class='col-md-6 offset-md-3 mb-3') for field in self.fields],
            Submit('submit', 'Save', css_class='btn btn-dark mt-3 mb-3 col-md-6 offset-md-3')
        )

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h1 class="text-center">Section Form</h1>'),
            *[Div(InlineField(field), css_class='col-md-6 offset-md-3 mb-3') for field in self.fields],
            Submit('submit', 'Save', css_class='btn btn-dark mt-3 mb-3 col-md-6 offset-md-3')
        )
