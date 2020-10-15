import qrcode
import fitz
import zipfile
import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from django.conf import settings
from .models import Position, Detail, Order, Fields_Position, Operation


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def qr_generator(title):
    host = settings.ALLOWED_HOSTS[0]
    detail_view_url = 'http://' + str(host) + ':9997' + '/all/Position/' + title
    #detail_view_url = 'http://127.0.0.1:8000/all/Position/' + title
    text = str(title)
    img = qrcode.make(detail_view_url)
    img_path = os.path.join(BASE_DIR, 'media/QR_CODE/') + text + '.png'
    try:
        img.save(img_path)
        
        # filename convert
        img_name = 'media/QR_CODE/' + text + '.png'
        print(img_path, '>', img_name)
        
    except:
        print('Error save')
    return img_name


def convert_pdf_to_bnp(infile, outfile):
    doc = fitz.open(infile)
    page = doc.loadPage(0)
    pix = page.getPixmap()
    output = outfile
    pix.writePNG(output)


def create_pdf(order):
    positions = Position.objects.filter(order=order)
    f_n = (str(order.title) + " #" + str(order.pk))
    file_name = os.path.join(BASE_DIR, 'media/QR_CODE_LIST/') + '{}.pdf'.format(f_n)

    # filename convert
    new_file_name = 'media/QR_CODE_LIST/' + '{}.pdf'.format(f_n)
    print(file_name, '>', new_file_name)

    documentTitle = '{} #{}'.format(order.title, order.pk)
    pdf = canvas.Canvas(file_name)
    pdfmetrics.registerFont(TTFont('FreeSans', os.path.join(BASE_DIR, 'MainApp/FreeSans.ttf')))
    canvas.Canvas.setFont(pdf, 'FreeSans', 8)
    pdf.setTitle(documentTitle)
    masshtab = 2.834
    pdf.rect(0, 0, 210 * masshtab, 297 * masshtab, stroke=1, fill=0)
    order = str(order.title)

    def crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img):
        pdf.rect(x, y, 44 * masshtab, 20 * masshtab, stroke=1, fill=0)
        canvas.Canvas.drawImage(pdf, img, x + 21.3 * masshtab, y - 1.5 * masshtab, width=23.2 * masshtab,
                                height=23.2 * masshtab)
        canvas.Canvas.setFont(pdf, 'FreeSans', 8)
        if len(detail_title) > 15:
            pdf.drawString(x + 1 * masshtab, y + 1 * masshtab, detail_title[15:30])
            pdf.drawString(x + 1 * masshtab, y + 4 * masshtab, detail_title[0:15])
        else:
            pdf.drawString(x + 1 * masshtab, y + 3 * masshtab, detail_title)
        canvas.Canvas.setFont(pdf, 'FreeSans', 6)
        pdf.drawString(x + 1 * masshtab, y + 8 * masshtab, 'НАЗВАНИЕ ДЕТАЛИ:')
        canvas.Canvas.setFont(pdf, 'FreeSans', 6)
        pdf.drawString(x + 1 * masshtab, y + 10.5 * masshtab, str("КОЛ-ВО: " + position_quantity))  # +
        canvas.Canvas.setFont(pdf, 'FreeSans', 6)
        if len(order) > 16:
            pdf.drawString(x + 1 * masshtab, y + 15 * masshtab, order[0:18])
            pdf.drawString(x + 1 * masshtab, y + 13 * masshtab, order[18:36])
        else:
            pdf.drawString(x + 1 * masshtab, y + 14 * masshtab, order)
        canvas.Canvas.setFont(pdf, 'FreeSans', 6)
        pdf.drawString(x + 1 * masshtab, y + 17.5 * masshtab, 'НАЗВАНИЕ ЗАКАЗА:')  # +

    i = 0

    y0 = 15
    x0 = 15
    dx = 52.5 * masshtab
    dy = 29.7 * masshtab

    for position in positions:
        i += 1

    a = 3
    b = i // a

    k = 0
    t = 0
    g = 0
    h = 0

    for position in positions:
        detail_title = str(position.detail.title)
        position_code = str(position.code)
        position_quantity = str(position.quantity)
        order_title = str(order.title)
        img = str(position.qr_code).replace('\\', '/')
        if h % 40 == 0 and h != 0:
            k = 0
            g = 0
            t = 0
            canvas.Canvas.showPage(pdf)
            pdfmetrics.registerFont(TTFont('FreeSans', os.path.join(BASE_DIR, 'MainApp/FreeSans.ttf')))
            canvas.Canvas.setFont(pdf, 'FreeSans', 8)
        if k > 3:
            k = 0
        x = x0 + dx * k
        if t % 4 == 0 and t != 0:
            g += 1
        y = y0 + dy * g
        k += 1
        t += 1
        h += 1
        crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img)

    pdf.save()

    return new_file_name


def detail_check(title):
    try:
        detail = Detail.objects.get(title=title)
        ex_check = True
    except:
        ex_check = False
    return ex_check


def pdf_draw_check(title):
    try:
        detail = Detail.objects.get(title=title)
        detail_draw = detail.draw_pdf
        print(detail_draw)
        ex_check = True
    except:
        ex_check = False
        print(ex_check)
    return ex_check


def ex_archive(order):  # Распковка архива и присвоение чертежей деталям.
    ex_order = Order.objects.get(pk=order.pk)
    ex_order.archive_ready = False
    ex_order.save()
    zip_archive = zipfile.ZipFile(ex_order.draw_archive, 'r')
    pdf_path = os.path.join(BASE_DIR, 'media/PDF_DRAW/')
    none_detail = []
    yes_detail = []
    sushest_detail = []
    for title in zip_archive.namelist():
        print(title)
        if os.path.exists(pdf_path + title):
            title = title.encode('cp437').decode('cp866')
            print('yes')
            sushest_detail.append(title)
        else:
            print('no')
            zip_archive.extract(title, pdf_path)
            file_path = pdf_path + title
            title = Path(title.encode('cp437').decode('cp866'))
            draw_path = str(pdf_path) + str(title)
            draw_path = draw_path.replace('\\', '/')
            os.rename(file_path, draw_path)
            title = str(title)[0:-4]
            pdf_draw_check(title)
            d_check = detail_check(title)
            if d_check:
                detail = Detail.objects.get(title=title)
                yes_detail.append(title)
                detail.draw_pdf = draw_path
                png_file_name = title + '.png'
                png_full_path = os.path.join(BASE_DIR, 'media/PNG_COVER/') + png_file_name
                convert_pdf_to_bnp(detail.draw_pdf.path, png_full_path)
                png_path_name = 'PNG_COVER/' + png_file_name
                detail.draw_png = png_path_name
                detail.save()
            else:
                none_detail.append(title)
                os.remove(draw_path)

    return none_detail, yes_detail, sushest_detail


def pdf_archive_form(url):
    order = Order.objects.get(pk=url)
    positions = Position.objects.filter(order=order)
    old_archive_path = order.draw_archive.path  # Удалить послез перезаписи нового
    archive_name = str(order.title) + " " \
                   + (str(datetime.datetime.now())).replace('-', '').replace(':', ''). \
                       replace('.', '').replace(' ', '') + '.zip'
    new_archive_path = os.path.join(BASE_DIR, 'media/DRAW_ARCHIVE/') + archive_name
    archive = zipfile.ZipFile(new_archive_path, mode='w')
    for position in positions:
        try:
            print('create')
            if position.detail.draw_pdf == 'PDF_DRAW/default.pdf':
                print('continue')
                continue
            else:
                archive.write(position.detail.draw_pdf.path)
                print('wright')
        finally:
            print('close')
    archive.close()
    archive_name = 'media/DRAW_ARCHIVE/' + archive_name
    print(archive_name)
    order.draw_archive = archive_name
    order.archive_ready = True
    order.save()
    os.remove(old_archive_path)

    return True
