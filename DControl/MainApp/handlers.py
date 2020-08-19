import qrcode
import fitz
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Position

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
    b = i//a

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
