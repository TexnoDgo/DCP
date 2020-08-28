from django.contrib import admin
from django.urls import path
from .views import detail_create, details_all, order_create, order_super_create,\
    orders_all, order_view, position_view, operation_view, archive_pdf_former, position_draw_change


urlpatterns = [
    path('AllDetails', details_all, name='details_all'),
    path('DetailCreate', detail_create, name='detail_create'),
    path('AllOrders', orders_all, name='orders_all'),
    path('OrderCreate', order_create, name='order_create'),
    path('OrderSuperCreate', order_super_create, name='order_super_create'),
    path(r'Order/<slug:url>', order_view, name='order_view'),
    path(r'Position/<slug:code>', position_view, name='position_view'),
    path(r'Position/<slug:code>/position_draw_change', position_draw_change, name='position_draw_change'),
    
    path(r'Operation/<slug:url>', operation_view, name='operation_view'),
    path(r'archive_pdf_former/<slug:url>', archive_pdf_former, name='archive_pdf_former'),
]
