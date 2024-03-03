from django.urls import path
from .views import (ActivateTableOrderView,
                    ActiveDashboardView,
                    AvailableSectionsView,
                    AvailableTablesView,
                    CreateTableView,
                    DeleteOrderItemView,
                    DeliverOrderItemView,
                    FinalizeOrderView,
                    FinishOpenOrdersView,
                    HistoricalOrdersView,
                    MenuCategoryCreateView,
                    MenuCategoryDeleteView,
                    MenuCategoryListView,
                    MenuCategoryUpdateView,
                    MenuItemListView,
                    OpenOrdersView,
                    OrderDetailView,
                    OrderItemCreateView,
                    PaidOrderView,
                    PartialOrderItemsListDeleteView,
                    PartialOrderItemsListView,
                    ProductDeleteView,
                    ProductListView,
                    ProductProfileCreateView,
                    ProductProfileDeleteView,
                    ProductProfileEditView,
                    ProductProfileView,
                    ProductProfileFilesView,
                    ProductUpdateView,
                    SectionCreateView,
                    SectionDetailView,
                    SectionUpdateView,
                    SectionDeleteView,
                    SectionListView,
                    SwitchOrderTableView,
                    TableDeleteView,
                    TableDetailView,
                    TableEditView,
                    TablesbySectionView,
                    MenuCategoryFilesView,
                    MenuItemFilesView,
                    UndeliveredItemsView,
                    ChartsView,)

urlpatterns = [
    path('', ActiveDashboardView.as_view(), name='home-view'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail-view'),
    path('order/partial/delete', PartialOrderItemsListDeleteView.as_view(), name='partial-order-items-list-delete-view'),
    path('order/partial/', PartialOrderItemsListView.as_view(), name='partial-order-items-list-view'),
    path('order/paid/', PaidOrderView.as_view(), name='paid-order-view'),
    path('order/open/', OpenOrdersView.as_view(), name='open-orders-view'),
    path('order/finalize/<int:order_id>/', FinalizeOrderView.as_view(), name='finalize-order-view'),
    path('order/finish-all/', FinishOpenOrdersView.as_view(), name='finish-open-orders-view'),
    path('order/historical/', HistoricalOrdersView.as_view(), name='historical-orders-view'),
    ### OrderItem URLs
    path('order_item/create/<int:item_id>/', OrderItemCreateView.as_view(), name='order-item-create-view'),
    path('order_item/deliver/<int:item_id>/', DeliverOrderItemView.as_view(), name='deliver-order-item-view'),
    path('order_item/delete/<int:item_id>/', DeleteOrderItemView.as_view(), name='delete-order-item-view'),
    path('order_item/undelivered/', UndeliveredItemsView.as_view(), name='undelivered-items-view'),
    ### Table URLs
    path('tables/', TablesbySectionView.as_view(), name='tables-by-section-view'),
    path('tables/<int:table_id>/', TableDetailView.as_view(), name='table-detail-view'),
    path('tables/<int:table_id>/edit/', TableEditView.as_view(), name='table-edit-view'),
    path('tables/create/', CreateTableView.as_view(), name='create-table-view'),
    path('tables/available/<int:section_id>', AvailableTablesView.as_view(), name='available-tables-view'),
    path('tables/delete/<int:table_id>/', TableDeleteView.as_view(), name='table-delete-view'),
    path('tables/activate/<int:table_id>/', ActivateTableOrderView.as_view(), name='activate-table-order-view'),
    path('tables/switch/<int:table_id>/', SwitchOrderTableView.as_view(), name='switch-table-order-view'),

    ### Section URLs
    path('section/', SectionListView.as_view(), name='section-list-view'),
    path('section/available/', AvailableSectionsView.as_view(), name='available-sections-view'),
    path('section/<int:section_id>/', SectionDetailView.as_view(), name='section-detail-view'),
    path('section/create/', SectionCreateView.as_view(), name='section-create-view'),
    path('section/<int:section_id>/update/', SectionUpdateView.as_view(), name='section-update-view'),
    path('section/<int:section_id>/delete/', SectionDeleteView.as_view(), name='section-delete-view'),

    ### Product URLs
    path('products/', ProductListView.as_view(), name='product-list-view'),
    path('products/create/', ProductProfileCreateView.as_view(), name='product-create-view'),
    path('products/<slug:handle>/',ProductProfileView.as_view(), name='product-profile-view'),
    path('products/<slug:handle>/files/', ProductProfileFilesView.as_view(), name='product-profile-files-view'),
    path('products/<slug:handle>/edit',ProductProfileEditView.as_view(), name='product-profile-edit-view'),
    path('products/<slug:handle>/delete/',ProductProfileDeleteView.as_view(), name='product-profile-delete-view'),
    path('products/update/<int:product_id>/', ProductUpdateView.as_view(), name='product-update-view'),
    path('products/delete/<int:product_id>/', ProductDeleteView.as_view(), name='product-delete-view'),
    
    ### MenuCategory URLs
    path('menu/', MenuCategoryListView.as_view(), name='menu-category-list-view'),
    path('menu/files/img/<int:category_id>/', MenuCategoryFilesView.as_view(), name='menu-category-files-view'),
    path('menu/<str:category_handle>/', MenuItemListView.as_view(), name='menu-item-list-view'),
    path('menu-item/files/img/<int:menu_item_id>/', MenuItemFilesView.as_view(), name='menu-item-files-view'),
    path('menu-category/create/', MenuCategoryCreateView.as_view(), name='menu-category-create-view'),
    path('menu-category/update/<int:category_id>/', MenuCategoryUpdateView.as_view(), name='menu-category-update-view'),
    path('menu-category/delete/<int:category_id>/', MenuCategoryDeleteView.as_view(), name='menu-category-delete-view'),
    
    ### Charts
    path('charts/', ChartsView.as_view(), name='charts-view'),
]
