from django.shortcuts import render, redirect
from django.views import View
from shop.models import Order, OrderItem, MenuCategory, MenuItem, Table
from shop.forms import OrderItemForm


# Create your views here.

def home(request):
    context = {}
    return render(request, 'pages/home.html', context=context)


class ActiveDashboardView(View):
    """Home View that includes active orders and undelivered items."""

    def get(self, request):
        qs = request.GET.get('q')
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
        return render(request, 'pages/home.html', context=context)


class OrderDetailView(View):
    """View for order details."""

    def get(self, request, order_id):
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

    def get(self, request, category_handle):
        category = MenuCategory.objects.get(handle=category_handle)
        items = category.menuitem_set.all()
        context = {
            'category': category,
            'items': items
        }
        return render(request, 'partials/menu_items_list.html', context=context)


class OrderItemCreateView(View):
    """View for creating order item."""

    def get(self, request, item_id):
        order = request.order
        item = MenuItem.objects.get(id=item_id)
        print(item)
        form = OrderItemForm()
        context = {
            'form': form,
            'order': order,
            'item': item
        }
        return render(request, 'forms/add_order_item_form.html', context=context)

    def post(self, request, item_id):
        """If there's a quantity as a query parameter, use that. Otherwise, use the form."""
        order = request.order
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
    
class ActivateTableOrderView(View):
    """View for activating table order."""

    def post(self, request, table_id):
        table = Table.objects.get(id=table_id)
        table.in_use = True
        table.save()
        order = Order.objects.create(table=table)
        order.save()
        return redirect('home-view')
    
class DeliverOrderItemView(View):
    """View for delivering order item."""

    def post(self, request, item_id):
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

    def post(self, request, item_id):
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
        return redirect('home-view')