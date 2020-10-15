from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import detail_create, details_all, order_create, order_super_create,\
    orders_all, order_view, position_view, operation_view, archive_pdf_former, position_draw_change,\
    manufactured_acc, in_made_status, ready_status, PositionUpdate, DetailUpdate, detail_view, operation_add,\
    OperationDelete, order_operation_change_status, bambardier, fp_view, add_pisition, blog_create

urlpatterns = [
    path('AllDetails', details_all, name='details_all'),
    path('DetailCreate', detail_create, name='detail_create'),
    path(r'Detail/<slug:url>', detail_view, name='detail_view'),
    
    path(r'Detail/^(?P<pk>\d+)/update', DetailUpdate.as_view(template_name='MainApp/DetailUpdate.html'), name='detail_update'),
    
    path('AllOrders', orders_all, name='orders_all'),
    path('OrderCreate', order_create, name='order_create'),
    path('OrderSuperCreate', order_super_create, name='order_super_create'),
    path(r'Order/<slug:url>', fp_view, name='order_view'),
    path(r'Order/<slug:url>/add_pisition', add_pisition, name='add_pisition'),
    
    path(r'Fp_view/<slug:url>', fp_view, name='fp_view'),
    
    path(r'Position/<slug:code>', position_view, name='position_view'),
    
    path(r'Position/^(?P<pk>\d+)/update', PositionUpdate.as_view(template_name='MainApp/PositionUpdate.html'), name='position_update'),
    
    path(r'Position/<slug:code>/position_draw_change', position_draw_change, name='position_draw_change'),
    
    path(r'Position/<slug:code>/operationADD', operation_add, name='operation_add'),
    path(r'Operation/(?P<pk>\d+)/operationDELETE', OperationDelete.as_view(template_name='MainApp/OperationDelete.html'), name='operation_delete'),
    
    path(r'Operation/<slug:url>', operation_view, name='operation_view'),
    
    path(r'Operation/<slug:url>/status/made', in_made_status, name='in_made_status'),
    path(r'Operation/<slug:url>/status/ready', ready_status, name='ready_status'),
    path(r'Operation/<slug:url>/order_change', order_operation_change_status, name='order_operation_change_status'),
    
    path(r'archive_pdf_former/<slug:url>', archive_pdf_former, name='archive_pdf_former'),
    path(r'Manufactured/<slug:url>', manufactured_acc, name='manufactured'),
    
    path(r'bambardier', bambardier, name='bambardier'),
    
    path(r'blog_view', blog_create, name='blog_create'),
    
    
]
