from django.urls import path
from .views import home, ActiveDashboardView, OrderDetailView, MenuCategoryListView, MenuItemListView, OrderItemCreateView

urlpatterns = [
    path('', ActiveDashboardView.as_view(), name='home-view'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('menu/', MenuCategoryListView.as_view(), name='menu-category-list-view'),
    path('menu/<str:category_handle>/', MenuItemListView.as_view(), name='menu-item-list-view'),
    path('order_item/create/<int:item_id>/', OrderItemCreateView.as_view(), name='order-item-create-view'),

]
