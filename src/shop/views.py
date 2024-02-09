from django.shortcuts import render, redirect
from django.views import View
from shop.models import Order, OrderItem, MenuCategory, MenuItem, Table, Product
from shop.forms import OrderItemForm, ProductForm, MenuCategoryForm, MenuItemForm
from django.contrib import messages


# Create your views here.

def home(request):
    context = {}
    return render(request, 'pages/home.html', context=context)


class ActiveDashboardView(View):
    """Home View that includes active orders and undelivered items."""

    def get(self, request):
        active_orders = Order.objects.filter(is_finished=False)
        undelivered_items = OrderItem.objects.filter(
            order__is_finished=False, is_delivered=False)
        context = {
            'active_orders': active_orders,
            'undelivered_items': undelivered_items
        }
        try:
            del request.session['order_id']
        except:
            pass
        return render(request, 'pages/new_home.html', context=context)


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
        order = Order.objects.get(id=order_id)
        order_items = order.orderitem_set.all()
        context = {
            'order': order,
            'order_items': order_items
        }
        request.session['order_id'] = order_id
        return render(request, 'pages/order_detail.html', context=context)


class MenuCategoryListView(View):
    """View for menu category."""

    def get(self, request):
        categories = MenuCategory.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'partials/menu_categories_list.html', context=context)


class MenuItemListView(View):
    """View for menu item."""

    def get(self, request, category_handle:str):
        category = MenuCategory.objects.get(handle=category_handle)
        items = category.menuitem_set.all()
        context = {
            'category': category,
            'items': items
        }
        return render(request, 'partials/menu_items_list.html', context=context)


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
            messages.error(request, 'Order is already finalized.')
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


class AvailableTablesView(View):
    """View for available tables."""

    def get(self, request):
        available_tables = Table.objects.filter(in_use=False)
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
        return redirect('home-view')
    
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
        product = Product.objects.get(id=product_id)
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
    
class ProductDeleteView(View):
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
        form = MenuCategoryForm(request.POST)
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
        form = MenuCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('menu-category-list-view')
        context = {
            'form': form
        }
        return render(request, 'forms/object_form.html', context=context)
    
class MenuCategoryDeleteView(View):
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
        category = MenuCategory.objects.get(id=category_id)
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
    
class MenuItemDeleteView(View):
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
        item = MenuItem.objects.get(handle=item_handle)
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