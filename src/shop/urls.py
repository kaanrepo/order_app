from django.urls import path
from .views import (home, ActiveDashboardView, OrderDetailView, MenuCategoryListView,
                     MenuItemListView,OrderItemCreateView, AvailableTablesView, ActivateTableOrderView,
                       DeliverOrderItemView, DeleteOrderItemView, FinalizeOrderView,
                       ProductDetailView, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
                       MenuCategoryCreateView, MenuCategoryUpdateView, MenuCategoryDeleteView,MenuCategoryDetailView,
                       MenuItemCreateView, MenuItemUpdateView, MenuItemDeleteView, MenuItemDetailView, MenuItemListView,
                       PartialOrderItemsListDeleteView, SwitchOrderTableView, PaidOrderView, PartialOrderItemsListView, ProductProfileView,
                       ProductProfileEditView, ProductProfileCreateView, ProductProfileDeleteView,TablesbySectionView, CreateTableViev)

urlpatterns = [
    path('', ActiveDashboardView.as_view(), name='home-view'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('order/partial/delete', PartialOrderItemsListDeleteView.as_view(), name='partial-order-items-list-delete-view'),
    path('order/partial/', PartialOrderItemsListView.as_view(), name='partial-order-items-list-view'),
    path('order/paid/', PaidOrderView.as_view(), name='paid-order-view'),
    path('order/finalize/<int:order_id>/', FinalizeOrderView.as_view(), name='finalize-order-view'),
    path('order_item/create/<int:item_id>/', OrderItemCreateView.as_view(), name='order-item-create-view'),
    path('order_item/deliver/<int:item_id>/', DeliverOrderItemView.as_view(), name='deliver-order-item-view'),
    path('order_item/delete/<int:item_id>/', DeleteOrderItemView.as_view(), name='delete-order-item-view'),
    path('tables/', TablesbySectionView.as_view(), name='tables-by-section-view'),
    path('tables/create/', CreateTableViev.as_view(), name='create-table-view'),
    path('tables/available/', AvailableTablesView.as_view(), name='available-tables-view'),

    path('tables/activate/<int:table_id>/', ActivateTableOrderView.as_view(), name='activate-table-order-view'),
    path('tables/switch/<int:table_id>/', SwitchOrderTableView.as_view(), name='switch-table-order-view'),

    ### Product URLs
    path('products/', ProductListView.as_view(), name='product-list-view'),
    #path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail-view'),
    path('products/create/', ProductProfileCreateView.as_view(), name='product-create-view'),

    path('products/<slug:handle>/',ProductProfileView.as_view(), name='product-profile-view'),
    path('products/<slug:handle>/edit',ProductProfileEditView.as_view(), name='product-profile-edit-view'),
    path('products/<slug:handle>/delete/',ProductProfileDeleteView.as_view(), name='product-profile-delete-view'),

    path('products/update/<int:product_id>/', ProductUpdateView.as_view(), name='product-update-view'),
    path('products/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product-delete-view'),
    ### MenuCategory URLs
    path('menu/', MenuCategoryListView.as_view(), name='menu-category-list-view'),
    path('menu/<str:category_handle>/', MenuItemListView.as_view(), name='menu-item-list-view'),
    path('menu-category/<int:category_id>/', MenuCategoryDetailView.as_view(), name='menu-category-detail-view'),
    path('menu-category/create/', MenuCategoryCreateView.as_view(), name='menu-category-create-view'),
    path('menu-category/update/<int:category_id>/', MenuCategoryUpdateView.as_view(), name='menu-category-update-view'),
    path('menu-category/delete/<int:category_id>/', MenuCategoryDeleteView.as_view(), name='menu-category-delete-view'),
    ### MenuItem URLs
    path('menu-item/', MenuItemListView.as_view(), name='menu-item-list-view'),
    path('menu-item/<str:item_handle>/', MenuItemDetailView.as_view(), name='menu-item-detail-view'),
    path('menu-item/create/', MenuItemCreateView.as_view(), name='menu-item-create-view'),
    path('menu-item/update/<int:item_id>/', MenuItemUpdateView.as_view(), name='menu-item-update-view'),
    path('menu-item/delete/<int:item_id>/', MenuItemDeleteView.as_view(), name='menu-item-delete-view'),





]
