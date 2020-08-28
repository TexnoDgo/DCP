import os
from openpyxl import load_workbook
import urllib.request

from django.utils.crypto import get_random_string
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import (Material, Assortment, Detail,
                     Project, Order, Position, City,
                     Manufactured, Operation, Transaction, StockageCode, SystemFile)
from .forms import (ProjectCreateForm, MaterialCreateForm, AssortmentCreateForm,
                    DetailCreateForm, OrderCreateForm, OrderSuperCreateForm, OrderDRAWUploadForm,
                    PositionCreateForm, CityCreateForm, ManufacturedCreateForm, OperationCreateForm,
                    TransactionCreateForm, PositionStorageForm, PositionSearch, PositionDrawAdd)
from .handlers import convert_pdf_to_bnp, qr_generator, create_pdf, detail_check, ex_archive, pdf_archive_form

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    details = Detail.objects.all()
    detail_list = []
    for detail in details:
      detail_list.append(detail.title)
    all_pos = Position.objects.filter(detail=None)
    positions = None
    text = ''

    if request.method == 'GET':

        form = PositionSearch(request.GET)
        print('post')

        if form.is_valid():
            print('valid')
            my_request = form.cleaned_data.get('my_request', None)
            try:
                positions = Position.objects.filter(detail__title=my_request)
                print(len(positions))
                if len(positions) == 0:
                    text = 'Данная деталь отсутствует в системе'
            except:
                print('ex')
                text = 'Данная деталь отсутствует в системе'
                messages.success(request,
                                 # Формирование сообщения со вложенным именем
                                 f'Данной детали не существует. ')

    else:
        form = PositionSearch()
    print(text)
    context = {
        'details': details,
        'form': form,
        'all_pos': positions,
        'text': text,
        'detail_list': detail_list,
    }
    return render(request, 'MainApp/HomePage.html', context)


@login_required
def detail_create(request):
    if request.method == "POST":

        form = DetailCreateForm(request.POST, request.FILES)
        print('post')

        if form.is_valid():
            detail = form.save(commit=False)
            detail.author = request.user
            form.save()
            pdf_file_name = str(detail.draw_pdf)
            print(pdf_file_name)  # Delete
            png_file_name = '{}{}'.format(pdf_file_name[9:-3], 'png')
            print(png_file_name)  # Delete
            png_full_path = os.path.join(BASE_DIR, 'media/PNG_COVER/') + png_file_name
            print(png_full_path)  # Delete
            convert_pdf_to_bnp(detail.draw_pdf.path, png_full_path)
            png_path_name = 'PNG_COVER/' + png_file_name
            print(png_path_name)
            detail.draw_png = png_path_name
            detail.save()
            print('valid')
            return redirect('detail_all')
    else:

        form = DetailCreateForm()
        print('else')

    context = {
        'form': form,
    }

    return render(request, 'MainApp/Detail_Create.html', context)


@login_required
def details_all(request):
    all_detail = Detail.objects.all()

    context = {
        'all_detail': all_detail,
    }
    return render(request, 'MainApp/All_Details.html', context)


@login_required
def order_create(request):

    if request.method == "POST":

        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.save()
            return redirect('orders_all')
    else:
        form = OrderCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'MainApp/Order_Create.html', context)


@login_required
def order_super_create(request):
    if request.method == 'POST':

        order_form = OrderSuperCreateForm(request.POST, request.FILES)

        if order_form.is_valid():
            super_order = order_form.save(commit=False)
            wb = load_workbook(super_order.table)
            sheet = wb['Лист1']
            # ----------------Информация о заказе----------------
            order_title = sheet.cell(row=2, column=2).value
            order_project = sheet.cell(row=3, column=2).value
            order_readiness = sheet.cell(row=4, column=2).value
            order_readiness = (str(order_readiness))[0:10]
            super_order.title = order_title
            super_order.author = request.user
            ex_project = Project.objects.get(title=order_project)
            super_order.project = ex_project
            super_order.readiness = order_readiness
            super_order.save()
            # ----------------Информация о заказе----------------

            # ----------------Информация по позициям----------------
            i = 1
            while i != 0:
                row_0 = 7
                col_0 = 5
                # Информация о детали
                detail_title = sheet.cell(row=row_0 + i, column=1).value
                detail_material = sheet.cell(row=row_0 + i, column=3).value
                detail_assortment = sheet.cell(row=row_0 + i, column=4).value
                detail_thickness_diameter = sheet.cell(row=row_0 + i, column=5).value
                # Информация о позициях
                position_quantity = sheet.cell(row=row_0 + i, column=2).value

                if detail_title is not None:
                    i += 1
                    print(detail_title)
                    ex_part = detail_check(detail_title)
                    print(ex_part)
                    # --------------------Создание детали-----------------------
                    ex_material = Material.objects.get(title=detail_material)
                    ex_assortment = Assortment.objects.get(title=detail_assortment)
                    ex_stockage_code = StockageCode.objects.get(title='Без расположения')
                    code = get_random_string(length=32)
                    qr_code = qr_generator(code)
                    if not ex_part:
                        # --------------------Создание детали-----------------------
                        detail = Detail(title=detail_title, author=request.user, material=ex_material,
                                        assortment=ex_assortment, thickness_diameter=detail_thickness_diameter)
                        detail.save()
                        # --------------------Создание детали-----------------------
                        # --------------------Создание позиции-----------------------
                        position = Position(order=super_order, detail=detail, quantity=position_quantity,
                                            code=code, qr_code=qr_code, stockage_code=ex_stockage_code)
                        # --------------------Создание позиции-----------------------
                    elif ex_part:
                        detail = Detail.objects.get(title=detail_title)
                        position = Position(order=super_order, detail=detail, quantity=position_quantity,
                                            code=code, qr_code=qr_code, stockage_code=ex_stockage_code)
                    else:
                        print('IF error')

                    position.save()

                    # ----------------------Информация об операциях-----------------
                    for a in range(1, 8):
                        operation = sheet.cell(row=row_0 + i - 1, column=col_0 + a).value
                        operation_manufactured = sheet.cell(row=7, column=col_0 + a).value
                        if operation is not None:
                            ex_manufactured = Manufactured.objects.get(title=operation_manufactured)
                            ex_opertion = Operation(manufactured=ex_manufactured, position=position,
                                                    remaining_parts=position_quantity)
                            ex_opertion.save()
                    # ----------------------Информация об операциях-----------------
                else:
                    i = 0
            # ----------------Информация по позициям----------------
            pdf_file_path = create_pdf(super_order)
            super_order.qr_code_list = pdf_file_path
            super_order.save()
            return redirect('orders_all')
    else:
        order_form = OrderSuperCreateForm()

    context = {
        'order_form': order_form,
    }

    return render(request, 'MainApp/Order_Super_Create.html', context)


@login_required
def orders_all(request):

    all_orders = Order.objects.all()

    '''orders = {}
    for order in all_orders:
        orders = order.title
        positions = Position.objects.filter(order=order)
        position_quantity = 0
        for position in positions:
            position_quantity += position.quantity
            operations = Operation.objects.filter(position=position)
            operation_remaining_parts = 0
            for operation in operations:
                operation_remaining_parts += int(operation.remaining_parts)
            orders[order.title]['rem'] = operation_remaining_parts
            orders[order.title]['qua'] = position_quantity
        print(orders)'''

    context = {
        'all_orders': all_orders,
    }

    return render(request, 'MainApp/All_Orders.html', context)


@login_required
def order_view(request, url):
    order = Order.objects.get(pk=url)
    positions = Position.objects.filter(order=order)
    details = Detail.objects.all()
    operations = Operation.objects.all()

    ready_positions = {}

    for position in positions:
        order_operations = Operation.objects.filter(position=position)
        ready_operations = 0
        for operation in order_operations:
            ready_operations += int(operation.remaining_parts)
        ready_positions[position.detail.title] = ready_operations

    print(ready_positions)

    if request.method == 'POST':

        form = OrderDRAWUploadForm(request.POST, request.FILES)

        if form.is_valid():
            archive = form.cleaned_data.get('archive', None)
            flag = form.cleaned_data.get('flag', None)
            order.draw_archive = archive
            order.save()
            if flag:
                print(ex_archive(order))
            return redirect(request.META['HTTP_REFERER'])
    else:

        form = OrderDRAWUploadForm()

    context = {
        'order': order,
        'positions': positions,
        'details': details,
        'operations': operations,
        'form': form,
        'ready_positions': ready_positions,
    }

    return render(request, 'MainApp/Order.html', context)


@login_required
def position_view(request, code):
    position = Position.objects.get(code=code)
    operations = Operation.objects.filter(position=position.pk)
    order = Order.objects.get(pk=position.order.pk)
    detail = Detail.objects.get(pk=position.detail.pk)
    maps = SystemFile.objects.get(title='maps')
    stockage = StockageCode.objects.all()

    if request.method == 'POST':

        form = PositionStorageForm(request.POST)

        if form.is_valid():
            position_in = form.cleaned_data.get('position_in', None)
            print(position_in)
            try:
                stockage = StockageCode.objects.get(title=position_in)
                position.stockage_code = stockage
                position.save()
            except:
                messages.success(request,
                                 # Формирование сообщения со вложенным именем
                                 f'Данного места не существует. ')

            return redirect(request.META['HTTP_REFERER'])
    else:
        form = PositionStorageForm()

    context = {
        'position': position,
        'operations': operations,
        'order': order,
        'detail': detail,
        'form': form,
        'maps': maps,
        'stockage': stockage,
    }

    return render(request, 'MainApp/Position.html', context)


@login_required
def position_draw_change(request, code):
    position = Position.objects.get(code=code)
    detail = Detail.objects.get(pk=position.detail.pk)
    
    if request.method == 'POST':
        print('post')
        
        form = PositionDrawAdd(request.POST, request.FILES)
        
        if form.is_valid():
            draw = form.cleaned_data.get('draw', None)
            print(draw)
            print('YES!')
            pdf_file_name = str(detail.draw_pdf)
            print(pdf_file_name)  # Delete
            png_file_name = '{}{}'.format(pdf_file_name[9:-3], 'png')
            print(png_file_name)  # Delete
            png_full_path = os.path.join(BASE_DIR, 'media/PNG_COVER/') + png_file_name
            print(png_full_path)  # Delete
            convert_pdf_to_bnp(detail.draw_pdf.path, png_full_path)
            png_path_name = 'PNG_COVER/' + png_file_name
            print(png_path_name)
            detail.draw_png = png_path_name
            detail.save()
            
            return redirect('position_view', code)
    
    else:
        print('else')
        form = PositionDrawAdd()
    
    context = {
      'position': position,
      'detail': detail,
      'form': form,
    }
    
    return render(request, 'MainApp/PositionDrawAdd.html', context)
        


@login_required
def operation_view(request, url):
    operation = Operation.objects.get(pk=url)
    transactions = Transaction.objects.filter(operation=operation)

    difference = int(operation.position.quantity) - int(operation.remaining_parts)

    if request.method == 'POST':

        form = TransactionCreateForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.author = request.user
            transaction.operation = operation
            print(operation.remaining_parts)
            if transaction.ready_quantity <= operation.remaining_parts:
                operation.remaining_parts -= transaction.ready_quantity
                print(operation.remaining_parts)
                operation.status = 'PD'
                if operation.remaining_parts == 0:
                    operation.status = 'RD'
                transaction.save()
                operation.save()
            else:
                messages.success(request,
                                 # Формирование сообщения со вложенным именем
                                 f'Количество выполненных деталей больше необходимого. '
                                 f'Пожалуйста проверьте вводимое значение или обратитесь '
                                 f'к автору заказа! ')

            return redirect(request.META['HTTP_REFERER'])
    else:

        form = TransactionCreateForm()

    context = {
        'operation': operation,
        'form': form,
        'difference': difference,
        'transactions': transactions,
    }
    return render(request, 'MainApp/Operation.html', context)


def crete_order_qr_code_list(request, url):
    order = Order.objects.get(pk=url)
    create_pdf(order)
    return redirect(request.META['HTTP_REFERER'])


def archive_pdf_former(request, url):
    order = Order.objects.get(pk=url)
    if order.draw_archive:
        pdf_archive_form(url)
    else:
        messages.success(request,
                         # Формирование сообщения со вложенным именем
                         f'Архив с чертежами отсутствует!.')
    # ADD MESSAGE
    return redirect(request.META['HTTP_REFERER'])
