import qrcode
import fitz
from django.conf import settings


def qr_generator(title):
    detail_view_url = 'localhost:8000/detail/'
    text = str(title)
    print(text)
    img = qrcode.make(detail_view_url + text)
    img_path = settings.MEDIA_URL + '/' + text + '.png'
    print(img_path)
    img2 = text + '.png'
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


