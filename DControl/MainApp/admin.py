from django.contrib import admin
from .models import (Material, Assortment, Detail, Project, Order, Position, City,
                     Manufactured, Operation, Transaction, StockageCode)

admin.site.register(Material)
admin.site.register(Assortment)
admin.site.register(Detail)
admin.site.register(Project)
admin.site.register(Order)
admin.site.register(Position)
admin.site.register(City)
admin.site.register(Manufactured)
admin.site.register(Operation)
admin.site.register(Transaction)
admin.site.register(StockageCode)
