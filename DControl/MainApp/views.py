import os
from openpyxl import load_workbook

from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import (Material, Assortment, Detail,
                     Project, Order, Position, City,
                     Manufactured, Operation, Transaction)
from .forms import (ProjectCreateForm, MaterialCreateForm, AssortmentCreateForm,
                    DetailCreateForm, OrderCreateForm, OrderSuperCreateForm, PositionCreateForm,
                    CityCreateForm, ManufacturedCreateForm, OperationCreateForm,
                    TransactionCreateForm)
from .handlers import convert_pdf_to_bnp, qr_generator, create_pdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def details_all(request):
    all_detail = Detail.objects.all()
    context = {
        'all_detail': all_detail,
    }
    return render(request, 'MainApp/All_Details.html', context)


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
                col_0 = 4
                # Информация о детали
                detail_title = sheet.cell(row=row_0 + i, column=1).value
                print(detail_title)
                try:
                    prov = Detail.objects.filter(title=detail_title)
                    print('yes')
                except:
                    print('no')

                detail_material = sheet.cell(row=row_0 + i, column=3).value
                detail_assortment = sheet.cell(row=row_0 + i, column=4).value
                # Информация о позициях
                position_quantity = sheet.cell(row=row_0 + i, column=2).value

                if detail_title is not None:
                    i += 1

                    # --------------------Создание детали-----------------------
                    ex_material = Material.objects.get(title=detail_material)
                    ex_assortment = Assortment.objects.get(title=detail_assortment)
                    detail = Detail(title=detail_title, author=request.user, material=ex_material, assortment=ex_assortment)
                    detail.save()
                    # --------------------Создание детали-----------------------

                    # --------------------Создание позиции-----------------------
                    code = get_random_string(length=32)
                    qr_code = qr_generator(code)
                    position = Position(order=super_order, detail=detail, quantity=position_quantity, code=code, qr_code=qr_code)
                    position.save()
                    # --------------------Создание позиции-----------------------

                    # ----------------------Информация об операциях-----------------
                    for a in range(1, 8):
                        operation = sheet.cell(row=row_0 + i - 1, column=col_0 + a).value
                        operation_manufactured = sheet.cell(row=7, column=col_0 + a).value
                        if operation is not None:
                            ex_manufactured = Manufactured.objects.get(title=operation_manufactured)
                            ex_opertion = Operation(manufactured=ex_manufactured, position=position, remaining_parts=position_quantity)
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


def orders_all(request):

    all_orders = Order.objects.all()

    context = {
        'all_orders': all_orders,
    }

    return render(request, 'MainApp/All_Orders.html', context)


def order_view(request, url):
    order = Order.objects.get(pk=url)
    positions = Position.objects.filter(order=order)
    details = Detail.objects.all()
    operations = Operation.objects.all()
    context = {
        'order': order,
        'positions': positions,
        'details': details,
        'operations': operations,
    }

    return render(request, 'MainApp/Order.html', context)


def position_view(request, code):
    position = Position.objects.get(code=code)
    operations = Operation.objects.filter(position=position.pk)
    order = Order.objects.get(pk=position.order.pk)
    detail = Detail.objects.get(pk=position.detail.pk)

    context = {
        'position': position,
        'operations': operations,
        'order': order,
        'detail': detail,
    }

    return render(request, 'MainApp/Position.html', context)


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
