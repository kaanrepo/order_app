from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from shop.models import Order, OrderItem, MenuCategory, MenuItem, Table, Product, Section
from shop.forms import OrderItemForm, ProductForm, MenuCategoryForm, MenuItemForm, TableForm, SectionForm
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django_htmx.http import HttpResponseClientRedirect
import pathlib
import mimetypes
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDate, ExtractHour, TruncMonth
import plotly.express as px

### s3
import s3
from order.env import config
from django.contrib.auth.mixins import LoginRequiredMixin

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default=None)  


class ActiveDashboardView(View):
    """Home View that includes active orders and undelivered items."""

    def get(self, request):
        today = timezone.now().date()
        active_orders_today = Order.objects.filter(created__date=today)
        active_orders_week = Order.objects.filter(created__week=today.isocalendar()[1])
        total_gain = sum([order.total_bill for order in active_orders_today])
        active_orders = Order.objects.filter(is_finished=False)
        undelivered_items = OrderItem.objects.filter(
            order__is_finished=False, is_delivered=False)
        delivered_items_today = OrderItem.objects.filter(
            is_delivered=True, created__date=today
        )
        context = {
            'active_orders': active_orders,
            'undelivered_items': undelivered_items,
            'active_orders_today': active_orders_today,
            'active_orders_week': active_orders_week,
            'delivered_items_today': delivered_items_today,
            'total_gain': total_gain
        }
        try:
            del request.session['order_id']
        except:
            pass
        return render(request, 'pages/new_home.html', context=context)


class UndeliveredItemsView(View):
    """View for undelivered items."""

    def get(self, request):
        if not request.htmx:
            return redirect('home-view')
        undelivered_items = OrderItem.objects.filter(
            order__is_finished=False, is_delivered=False)
        context = {
            'undelivered_items': undelivered_items
        }
        return render(request, 'partials/undelivered_items_list.html', context=context)

class PartialOrderItemsListDeleteView(View):
    def get(self, request):
        order = request.order
        order_items = order.orderitem_set.all()
        context={
            'order': order,
            'order_items': order_items
        }
        return render(request, 'partials/order_items_list_delete.html', context)

class PartialOrderItemsListView(View):
    def get(self, request):
        order = request.order
        order_items = order.orderitem_set.all()
        context={
            'order': order,
            'order_items': order_items
        }
        return render(request, 'partials/order_items_list.html', context)

class OrderDetailView(View):
    """View for order details."""

    def get(self, request, order_id:int):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.orderitem_set.all()
        context = {
            'order': order,
            'order_items': order_items
        }
        request.session['order_id'] = order_id
        return render(request, 'pages/order_detail.html', context=context)


class MenuCategoryFilesView(View):
    def get(self, request, category_id:int):
        if not request.htmx:
            return redirect('menu-category-list-view')
        category = get_object_or_404(MenuCategory, id=category_id)
        if category.image:
            client = s3.S3Client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    default_bucket_name=AWS_STORAGE_BUCKET_NAME).client
            try:
                client.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=category.image.name)
                url = client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': AWS_STORAGE_BUCKET_NAME,
                        'Key': category.image.name
                    },
                    ExpiresIn=1000
                )
                is_image = True
            except:
                url = None
                is_image = False
        data = {
                'category': category,
                'is_image': is_image,
                'url': url

            }
        context = {
            'data': data
        }
        return render(request, 'partials/menu_category_files.html', context=context)

class MenuCategoryListView(View):
    """View for menu categories."""

    def get(self, request):
        qs = MenuCategory.objects.all()
        context = {
            'categories': qs,
        }
        if request.htmx:
            #context['order'] = request.order
            return render(request, 'partials/menu_categories_list.html', context=context)
        return render(request, 'pages/menu_categories_list.html', context=context)
    
class MenuItemFilesView(View):
    def get(self, request, menu_item_id:int):
        if not request.htmx:
            return redirect('menu-category-list-view')
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        if menu_item.product.image:
            client = s3.S3Client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                default_bucket_name=AWS_STORAGE_BUCKET_NAME).client
            try:
                client.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=menu_item.product.image.name)
                url = client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': AWS_STORAGE_BUCKET_NAME,
                        'Key': menu_item.product.image.name
                    },
                    ExpiresIn=1000
                )
                is_image = True
            except:
                url = None
                is_image = False
        data = {
            'menu_item': menu_item,
            'is_image': is_image,
            'url': url

        }
        context = {
            'data': data
        }
        return render(request, 'partials/menu_items_files.html', context=context)


class MenuItemListView(View):
    """View for menu item based on the selected category."""

    def get(self, request, category_handle:str):
        category = MenuCategory.objects.get(handle=category_handle)
        items = category.menuitem_set.all().filter(is_active=True)
        context = {
            'category': category,
            'items': items
        }
        if request.htmx:
            return render(request, 'partials/menu_items_list.html', context=context)
        return render(request, 'pages/menu_items_list.html', context=context)


class OrderItemCreateView(View):
    """View for creating order item."""

    def get(self, request, item_id:int):
        order = request.order
        item = MenuItem.objects.get(id=item_id)
        form = OrderItemForm()
        context = {
            'form': form,
            'order': order,
            'item': item
        }
        return render(request, 'forms/add_order_item_form2.html', context=context)

    def post(self, request, item_id:int):
        """If there's a quantity as a query parameter, use that. Otherwise, use the form."""
        order = request.order
        if order.is_finished:
            messages.error(request, "Can't add Items, order is already finalized.")
            return render(request, 'partials/messages_template.html', {})
        order_items = order.orderitem_set.all()
        menu_item = MenuItem.objects.get(id=item_id)
        form = OrderItemForm(request.POST)
        quantity = request.GET.get('quantity')
        context = {
            'order': order,
            'order_items': order_items,
        }
        if quantity is not None:
            if all([quantity.isdigit(), int(quantity) > 0]):
                order_item = OrderItem.objects.create(
                    order=order, menu_item=menu_item, quantity=int(quantity))
                order_item.save()
                return render(request, 'partials/order_items_list.html', context)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            order_item = OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=quantity)
            order_item.save()
            return render(request, 'partials/order_items_list.html', context)


class OpenOrdersView(View):
    """View for open orders."""

    def get(self, request):
        active_orders = Order.objects.filter(is_finished=False)
        context = {
            'active_orders': active_orders
        }
        return render(request, 'partials/open_orders_list.html', context=context)
    
class AvailableSectionsView(View):
    """View for available sections."""

    def get(self, request):
        if not request.htmx:
            return redirect('home-view')
        sections = Section.objects.all()
        context = {
            'sections': sections
        }
        return render(request, 'partials/available_sections_list.html', context=context)

class AvailableTablesView(View):
    """View for available tables."""

    def get(self, request, section_id:int):
        available_tables = Table.objects.filter(section__id=section_id)
        context = {
            'available_tables': available_tables,
        }
        return render(request, 'partials/available_tables_list.html', context=context)
    
class SwitchOrderTableView(View):
    """View for switching table of order."""

    def post(self, request, table_id:int):
        order = request.order
        old_table = order.table
        new_table = Table.objects.get(id=table_id)
        order.table = new_table
        order.save()
        old_table.in_use = False
        old_table.save()
        new_table.in_use = True
        new_table.save()
        context = {
            'order': order
        }
        return render(request, 'partials/order_info.html', context)

    
class ActivateTableOrderView(View):
    """View for activating table order."""

    def post(self, request, table_id:int):
        table = Table.objects.get(id=table_id)
        table.in_use = True
        table.save()
        order = Order.objects.create(table=table)
        order.save()
        active_orders = Order.objects.filter(is_finished=False)
        context = {
            'active_orders': active_orders
        }

        return render(request, "partials/open_orders_list.html", context)
    


    
class DeliverOrderItemView(View):
    """View for delivering order item."""

    def post(self, request, item_id:int):
        order = request.order
        order_items = order.orderitem_set.all()
        order_item = OrderItem.objects.get(id=item_id)
        order_item.is_delivered = True
        order_item.save()
        context={
            'order': order,
            'order_items': order_items
        }
        return render(request, 'partials/order_items_list.html', context)
        #return redirect('order-detail-view', order_item.order.id)
    
class DeleteOrderItemView(View):
    """View for deleting order item."""

    def post(self, request, item_id:int):
        order = request.order
        if order.is_finished:
            messages.error(request, "Can't delete, order is already finalized.")
            return render(request, 'partials/messages_template.html', {})
        order_items = order.orderitem_set.all()
        order_item = OrderItem.objects.get(id=item_id)
        order_item.delete()
        context={
            'order': order,
            'order_items': order_items
        }
        return render(request, 'partials/order_items_list.html', context)
        #return redirect('order-detail-view', order_item.order.id)
    
class FinalizeOrderView(View):
    """View for finalizing order."""

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.is_finished = True
        order.save()
        table = order.table
        table.in_use = False
        table.save()
        context = {
            'order': order
        }
        return render(request, 'partials/order_info.html', context)

class PaidOrderView(View):
    """View for paid order."""

    def post(self, request):
        order = request.order
        order.is_paid = True
        order.save()
        context = {
            'order': order
        }
        return render(request, 'partials/order_info.html', context)

### Product CRUD Views

class ProductDetailView(View):
    """View for product details."""

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        context = {
            'product': product
        }
        return render(request, 'pages/product_detail.html', context=context)

class ProductListView(View):
    """View for listing products."""

    def get(self, request):
        qs = Product.objects.all()
        context = {
            'products': qs
        }
        return render(request, 'pages/product_list.html', context=context)

class ProductCreateView(View):
    """View for creating product."""

    def get(self, request):
        form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class ProductUpdateView(View):
    """View for updating product."""

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class ProductDeleteView(LoginRequiredMixin, View):
    raise_exception = True
    """View for deleting product."""

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('product-list-view')
    

### Menu Category CRUD Views

class MenuCategoryCreateView(View):
    """View for creating menu category."""

    def get(self, request):
        form = MenuCategoryForm()
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request):
        form = MenuCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu-category-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class MenuCategoryUpdateView(View):
    """View for updating menu category."""

    def get(self, request, category_id):
        category = MenuCategory.objects.get(id=category_id)
        form = MenuCategoryForm(instance=category)
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request, category_id):
        category = MenuCategory.objects.get(id=category_id)
        form = MenuCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('menu-category-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
   
class MenuCategoryDeleteView(LoginRequiredMixin, View):
    raise_exception = True
    """View for deleting menu category."""

    def post(self, request, category_id):
        category = MenuCategory.objects.get(id=category_id)
        category.delete()
        return redirect('menu-category-list-view')
    
    def get(self, request, category_id):
        category = MenuCategory.objects.get(id=category_id)
        context = {
            'object': category,
            'delete_view' : "menu-category-delete-view"
        }
        return render(request, 'forms/object_delete.html', context=context)
    
    
class MenuCategoryDetailView(View):
    """View for menu category details."""

    def get(self, request, category_id):
        category = get_object_or_404(MenuCategory, id=category_id)
        context = {
            'category': category
        }
        return render(request, 'partials/menu_category_detail.html', context=context)
    


class MenuItemCreateView(View):
    """View for creating menu item."""

    def get(self, request):
        form = MenuItemForm()
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request):
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu-item-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class MenuItemUpdateView(View):
    """View for updating menu item."""

    def get(self, request, item_id):
        item = MenuItem.objects.get(id=item_id)
        form = MenuItemForm(instance=item)
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)

    def post(self, request, item_id):
        item = MenuItem.objects.get(id=item_id)
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('menu-item-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class MenuItemDeleteView(LoginRequiredMixin, View):
    raise_exception = True
    """View for deleting menu item."""

    def post(self, request, item_id):
        item = MenuItem.objects.get(id=item_id)
        item.delete()
        return redirect('menu-item-list-view')
    
    def get(self, request, item_id):
        item = MenuItem.objects.get(id=item_id)
        context = {
            'object': item,
            'delete_view' : "menu-item-delete-view"
        }
        return render(request, 'forms/object_delete.html', context=context)

class MenuItemDetailView(View):
    """View for menu item details."""

    def get(self, request, item_handle):
        item = get_object_or_404(MenuItem, handle=item_handle)
        context = {
            'item': item
        }
        return render(request, 'partials/menu_items_detail.html', context=context)

class MenuItemListView2(View):
    """View for listing menu items."""

    def get(self, request):
        qs = MenuItem.objects.all()
        context = {
            'items': qs
        }
        return render(request, 'partials/menu_items_list.html', context=context)
    


class ProductProfileFilesView(View):
    def get(self, request, handle:str):
        if not request.htmx:
            return redirect('home-view')
        product = Product.objects.get(handle=handle)
        data = {}
        if product.image:
            client = s3.S3Client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    default_bucket_name=AWS_STORAGE_BUCKET_NAME).client
            try:
                client.head_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=product.image.name)
                url = client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': AWS_STORAGE_BUCKET_NAME,
                        'Key': product.image.name
                    },
                    ExpiresIn=1000
                )
                is_image = True
            except:
                url = None
                is_image = False
            data = {
                'product': product,
                'is_image': is_image,
                'url': url
            }

        context = {
            'data': data
        }
        return render(request, 'partials/product_profile_files.html', context=context)




class ProductProfileView(View):
    """View for Product and MenuItem in a single view"""

    def get(self, request, handle:str):
        product = Product.objects.get(handle=handle)
        menu_item = MenuItem.objects.get(product=product)
        context = {
            'product': product,
            'menu_item': menu_item
        }
        return render(request, 'pages/product_profile_page.html', context)
    

class ProductProfileEditView(View):

    def post(self, request, handle:str):
        product = Product.objects.get(handle=handle)
        menu_item = MenuItem.objects.get(product=product)
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        menu_item_form = MenuItemForm(request.POST, instance=menu_item)
        context = {
            'product_form': product_form,
            'menu_item_form': menu_item_form,
            'product': product
        }
        if all([product_form.is_valid(), menu_item_form.is_valid()]):
            product_form.save()
            menu_item_form.save()
            return redirect('product-profile-view', product.handle)
        return render(request, 'pages/product_create_page.html', context)
        
    def get(self, request, handle:str):
        product = Product.objects.get(handle=handle)
        menu_item = MenuItem.objects.get(product=product)
        product_form = ProductForm(instance=product)
        menu_item_form = MenuItemForm(instance=menu_item)
        context = {
            'product_form': product_form,
            'menu_item_form': menu_item_form,
            'product': product,
        }
        return render(request, 'pages/product_create_page.html', context)
    


class ProductProfileCreateView(View):
    def get(self, request):
        product_form = ProductForm()
        menu_item_form = MenuItemForm()
        context = {
            'product_form': product_form,
            'menu_item_form': menu_item_form
        }
        return render(request, 'pages/product_create_page.html', context)
    
    def post(self, request):
        product_form = ProductForm(request.POST, request.FILES)
        menu_item_form = MenuItemForm(request.POST)
        if all([product_form.is_valid(), menu_item_form.is_valid()]):
            product = product_form.save()
            menu_item = menu_item_form.save(commit=False)
            menu_item.product = product
            menu_item.save()
            return redirect('product-profile-view', product.handle)
        context = {
            'product_form': product_form,
            'menu_item_form': menu_item_form
        }
        return render(request, 'pages/product_create_page.html', context)
    

class ProductProfileDeleteView(LoginRequiredMixin, View):
    raise_exception=True

    def post(self, request, handle:str):
        product = Product.objects.get(handle=handle)
        menu_item = MenuItem.objects.get(product=product)
        product.delete()
        menu_item.delete()
        return redirect('product-list-view')
    

class TablesbySectionView(View):
    def get(self, request):
        tables_by_section = [table              
                            for section in Section.objects.all() 
                            for table in section.table_set.all()]
        tables_by_section = {section:section.table_set.all() for section in Section.objects.all()}
        context ={
            'tables_by_section': tables_by_section
        }
        return render(request, 'pages/tables_by_section_page.html', context=context)

class SectionListView(View):
    def get(self, request):
        qs = { section : section.table_set.all() for section in Section.objects.all() }
        context = {
            'qs': qs
        }
        return render(request, 'pages/section_list_page.html', context)

class SectionDetailView(View):
    def get(self, request, section_id:int):
        section = get_object_or_404(Section, id=section_id)
        tables = section.table_set.all()
        context = {
            'section': section,
            'tables': tables
        }
        return render(request, 'pages/section_detail_page.html', context)

class SectionCreateView(View):
    def get(self, request):
        context = {
            'form': SectionForm()
        }
        return render(request, 'forms/object_form.html', context=context)
    
    def post(self, request):
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables-by-section-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class SectionDeleteView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, section_id:int):
        section = get_object_or_404(Section, id=section_id)
        section.delete()
        return redirect('section-list-view')
    
class SectionUpdateView(View):
    def get(self, request, section_id:int):
        section = get_object_or_404(Section, id=section_id)
        form = SectionForm(instance=section)
        context = {
            'form': form,
            'section': section
        }
        if request.htmx:
            return render(request, 'forms/partial_object_form.html', context)
        return render(request, 'forms/object_form.html', context=context)
    
    def post(self, request, section_id:int):
        section = get_object_or_404(Section, id=section_id)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('section-detail-view', section.id)
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    


class CreateTableView(View):
    def get(self, request):
        form = TableForm()
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
    def post(self, request):
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables-by-section-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    

class TableDetailView(View):
    def get(self, request, table_id:int):
        table = get_object_or_404(Table, id=table_id)
        form = TableForm(instance=table)
        context = {
            'table': table,
            'form': form
        }
        return render(request, 'pages/table_detail_page.html', context=context)
    

class TableEditView(View):
    def get(self, request, table_id:int):
        table = get_object_or_404(Table, id=table_id)
        form = TableForm(instance=table)
        context = {
            'table': table,
            'form': form
        }
        return render(request, 'forms/table_edit_form.html', context=context)
    
    def post(self, request, table_id:int):
        table = get_object_or_404(Table, id=table_id)
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table-detail-view', table.id)
        context = {
            'table': table,
            'form': form
        }
        return render(request, 'partials/table_detail.html', context=context)
    
class TableDeleteView(LoginRequiredMixin, View):
    raise_exception = True

    def post(self, request, table_id:int):
        table = get_object_or_404(Table, id=table_id)
        table.delete()
        return redirect('tables-by-section-view')

class HistoricalOrdersView(View):
    def get(self, request):
        orders = Order.objects.all().order_by('-created')
        q = request.GET.get('q')
        if q:
            orders = orders.search(q)
        context = {
            'orders': orders
        }
        if request.htmx:
            return render(request, 'partials/historical_orders_list.html', context)
        return render(request, 'pages/historical_orders_page.html', context)
    
class FinishOpenOrdersView(View):
    def post(self, request):
        active_orders = Order.objects.filter(is_finished=False)
        for order in active_orders:
            order.is_finished = True
            order.save()
            table = order.table
            table.in_use = False
            table.save()
        return render(request, 'partials/open_orders_list.html', {})
    

class ChartsView(View):
    def get(self, request):
        if request.htmx:
            revenue_by_date = OrderItem.objects.annotate(
                date_only=TruncDate('created')
            ).values('date_only').annotate(revenue=Sum(F('menu_item__price') * F('quantity')))

            x = revenue_by_date.values_list('date_only', flat=True)
            y = revenue_by_date.values_list('revenue', flat=True)

            fig = px.line(
                x=x,
                y=y,
                labels={'x': 'Date', 'y': 'Revenue'},
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Revenue",
                dragmode=False,
            )
            fig.update_traces(mode="markers+lines", textposition='top center')
            chart = fig.to_html()

            quantity_by_product = OrderItem.objects.values('menu_item__product__name', 'menu_item__product__unit' , 'menu_item__product__size').annotate(quantity=Sum('quantity'))
            x1 = [f"{item['menu_item__product__name']} {item['menu_item__product__size']} {item['menu_item__product__unit']}" for item in quantity_by_product]
            y1 = quantity_by_product.values_list('quantity', flat=True)
            fig1 = px.bar(
                x=x1,
                y=y1,
                labels={'x': 'Product', 'y': 'Quantity'},
                text_auto=True,
            )
            fig1.update_traces(textposition='outside')
            fig1.update_layout(
                dragmode=False,
            )
            chart2 = fig1.to_html()

            orders_by_time = Order.objects.annotate(hour=ExtractHour('created')).values('hour').annotate(count=Count('id'))
            x2 = orders_by_time.values_list('hour', flat=True)
            y2 = orders_by_time.values_list('count', flat=True)
            fig2 = px.bar(
                x=x2,
                y=y2,
                labels={'x': 'Hour of the day', 'y': 'Orders'},
                text_auto=True,
            )
            fig2.update_layout(
                dragmode=False,
            )
            fig2.update_xaxes(
                range=[0, 24],
            )
            fig2.update_traces(textposition='outside')
            chart3 = fig2.to_html()

            revenue_by_category = OrderItem.objects.values('menu_item__category__name').annotate(revenue=Sum(F('menu_item__price') * F('quantity')))
            x3 = revenue_by_category.values_list('menu_item__category__name', flat=True)
            y3 = revenue_by_category.values_list('revenue', flat=True)
            fig3 = px.bar(
                x=x3,
                y=y3,
                labels={'x': 'Category', 'y': 'Revenue'},
                text_auto=True,
            )
            fig3.update_layout(
                dragmode=False,
            )

            fig3.update_traces(textposition='outside')

            chart4 = fig3.to_html()
            context = {
                'chart': chart,
                'chart2': chart2,
                'chart3': chart3,
                'chart4': chart4
            }
            return render(request, 'partials/charts_partial.html', context)


        return render(request, 'pages/charts_page.html', {})
    





