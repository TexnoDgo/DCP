import qrcode
import fitz
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def qr_generator(title):
    detail_view_url = 'http://127.0.0.1:8000/all/Position/' + title
    text = str(title)
    print(text)
    img = qrcode.make(detail_view_url)
    img_path = os.path.join(BASE_DIR, 'media/QR_CODE/') + text + '.png'
    print(img_path)
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


