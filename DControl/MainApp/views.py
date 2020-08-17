import os
from django.shortcuts import render, redirect
from .models import (Material, Assortment, Detail,
                     Project, Order, Position, City,
                     Manufactured, Operation, Transaction)
from .forms import (ProjectCreateForm, MaterialCreateForm, AssortmentCreateForm,
                    DetailCreateForm, OrderCreateForm, PositionCreateForm,
                    CityCreateForm, ManufacturedCreateForm, OperationCreateForm,
                    TransactionCreateForm)
from .handlers import convert_pdf_to_bnp

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


def detail_all(request):
    all_detail = Detail.objects.all()
    context = {
        'all_detail': all_detail,
    }
    return render(request, 'MainApp/All_Details.html', context)