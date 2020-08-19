from reportlab.pdfgen import canvas


file_name = 'C:/PP/DCProject/DCP/TestPart/MyPDF.pdf'
documentTitle = 'Order_Title + Order_pk'
img = 'C:/PP/DCProject/DCP/TestPart/jf669qNTpM2H5G92EllzGrpy6xptDnfM.png'


pdf = canvas.Canvas(file_name)
canvas.Canvas.setFont(pdf, "Times-Roman", 10)
pdf.setTitle(documentTitle)
masshtab = 2.834
pdf.rect(0, 0, 210*masshtab, 297*masshtab, stroke=1, fill=0)

'''
Функция Добавления одного кода
def funk():
    detail_title, position_code, position_quantity, order
1. Добавить рамку
2. Дабавить текст
3. Добавить код 
'''


def crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img):
    pdf.rect(x, y, 63.33 * masshtab, 31.5 * masshtab, stroke=1, fill=0)
    canvas.Canvas.drawImage(pdf, img, x+34.83*masshtab, y+3*masshtab, width=25.5 * masshtab, height=25.5 * masshtab)
    pdf.drawString(x+3*masshtab, y+3*masshtab, detail_title)
    pdf.drawString(x+3*masshtab, y+9.375*masshtab, position_code)
    pdf.drawString(x+3*masshtab, y+15.75*masshtab, position_quantity)
    pdf.drawString(x+3*masshtab, y+22.125*masshtab, order)


def create_pdf():
    detail_title = 'detail_title'  # получаем из цикла по заказу
    position_code = 'position_code'  # получаем из цикла по заказу
    position_quantity = 'position_quantity'  # получаем из цикла по заказу
    order = 'order'  # получаем из цикла по заказу
    img = 'C:/PP/DCProject/DCP/TestPart/jf669qNTpM2H5G92EllzGrpy6xptDnfM.png' # получаем из цикла по заказу
    x = 5 * masshtab
    y = 5 * masshtab
    crete_one_pos(x, y, detail_title, position_code, position_quantity, order, img)

create_pdf()
pdf.save()


