from django.shortcuts import render, redirect
from django.views import View
from shop.models import Order, OrderItem, MenuCategory, MenuItem
from shop.forms import OrderItemForm


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
        order = request.order
        menu_item = MenuItem.objects.get(id=item_id)
        form = OrderItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            order_item = OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=quantity)
            order_item.save()
            return redirect('order-detail-view', order.id)
        
            
        
