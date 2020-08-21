import qrcode
import fitz
import zipfile
import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Position, Detail, Order
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def qr_generator(title):
    detail_view_url = 'http://127.0.0.1:8000/all/Position/' + title
    text = str(title)
    img = qrcode.make(detail_view_url)
    img_path = os.path.join(BASE_DIR, 'media/QR_CODE/') + text + '.png'
    try:
        img.save(img_path)
    except:
        print('Error save')
    return img_path


def convert_pdf_to_bnp(infile, outfile):
    doc = fitz.open(infile)
    page = doc.loadPage(0)
    pix = page.getPixmap()
    output = outfile
    pix.writePNG(output)


def create_pdf(order):
    positions = Position.objects.filter(order=order)
    f_n = (str(order.title) + " #" + str(order.pk))
    file_name = 'C:/PP/DCProject/DCP/DControl/media/QR_CODE_LIST/{}.pdf'.format(f_n)
    documentTitle = '{} #{}'.format(order.title, order.pk)
    pdf = canvas.Canvas(file_name)
    pdfmetrics.registerFont(TTFont('FreeSans', 'C:/PP/DCProject/DCP/DControl/MainApp/FreeSans.ttf'))
    canvas.Canvas.setFont(pdf, 'FreeSans', 8)
    pdf.setTitle(documentTitle)
    masshtab = 2.834
    pdf.rect(0, 0, 210 * masshtab, 297 * masshtab, stroke=1, fill=0)
    order = str(order.title)

    def crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img):
        pdf.rect(x, y, 63.33 * masshtab, 31.5 * masshtab, stroke=1, fill=0)
        canvas.Canvas.drawImage(pdf, img, x + 34.83 * masshtab, y + 3 * masshtab, width=25.5 * masshtab,
                                height=25.5 * masshtab)
        canvas.Canvas.setFont(pdf, 'FreeSans', 4)
        pdf.drawString(x + 3 * masshtab, y + 3 * masshtab, detail_title)
        canvas.Canvas.setFont(pdf, 'FreeSans', 4)
        pdf.drawString(x + 3 * masshtab, y + 9.375 * masshtab, position_code)
        canvas.Canvas.setFont(pdf, 'FreeSans', 12)
        pdf.drawString(x + 3 * masshtab, y + 15.75 * masshtab, position_quantity)
        canvas.Canvas.setFont(pdf, 'FreeSans', 4)
        pdf.drawString(x + 3 * masshtab, y + 22.125 * masshtab, order)
        pdf.drawString(x + 3 * masshtab, y + 28.5 * masshtab, 'НАЗВАНИЕ ЗАКАЗА:')

    i = 0

    y0 = 5 * masshtab
    x0 = 5 * masshtab
    dx = 68.33 * masshtab
    dy = 36.5 * masshtab

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
        if h % 24 == 0 and h != 0:
            k = 0
            g = 0
            t = 0
            canvas.Canvas.showPage(pdf)
            pdfmetrics.registerFont(TTFont('FreeSans', 'C:/PP/DCProject/DCP/DControl/MainApp/FreeSans.ttf'))
            canvas.Canvas.setFont(pdf, 'FreeSans', 8)
        if k > 2:
            k = 0
        x = x0 + dx * k
        if t % 3 == 0 and t != 0:
            g += 1
        y = y0 + dy * g
        k += 1
        t += 1
        h += 1
        crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img)

    pdf.save()

    return file_name


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
        try:
            zip_archive.extract(title, pdf_path)
        except:
            sushest_detail.append(title)
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
    order.draw_archive = new_archive_path
    order.archive_ready = True
    order.save()
    os.remove(old_archive_path)

    return True
