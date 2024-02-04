from django.urls import path
from .views import home, ActiveDashboardView, OrderDetailView, MenuCategoryListView, MenuItemListView, OrderItemCreateView, AvailableTablesView, ActivateTableOrderView, DeliverOrderItemView

urlpatterns = [
    path('', ActiveDashboardView.as_view(), name='home-view'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('menu/', MenuCategoryListView.as_view(), name='menu-category-list-view'),
    path('menu/<str:category_handle>/', MenuItemListView.as_view(), name='menu-item-list-view'),
    path('order_item/create/<int:item_id>/', OrderItemCreateView.as_view(), name='order-item-create-view'),
    path('order_item/deliver/<int:item_id>/', DeliverOrderItemView.as_view(), name='deliver-order-item-view'),
    path('tables/', AvailableTablesView.as_view(), name='available-tables-view'),
    path('tables/activate/<int:table_id>/', ActivateTableOrderView.as_view(), name='activate-table-order-view'),

]
