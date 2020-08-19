from fpdf import FPDF

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size=10)


def draw_frame():
    pdf.set_line_width(1)
    pdf.set_fill_color(0, 255, 0)
    pdf.rect(0, 0, 210, 297)


def draw_code(x, y):
    pdf.set_line_width(1)
    pdf.set_fill_color(0, 255, 0)
    pdf.rect(x, y, 64, 31.5)


def create_order_details_frame():
    draw_frame()
    min_co = 4
    shag_gor = 69
    shag_vert = 36.5
    draw_code(min_co, min_co)
    for t in range(0, 8):
        for i in range(0, 3):
            print(i)
            draw_code(min_co + shag_gor * i, min_co + shag_vert*t)


img_path = 'C:/PP/DCProject/DCP/TestPart/jf669qNTpM2H5G92EllzGrpy6xptDnfM.png'


def add_qr_code_image(x, y, img_path):
    pdf.image(img_path, x=x, y=y, w=25.5)


def add_image_to_pdf(img_path):
    x0 = 39.85
    y0 = 8
    dx = 68.35
    dy = 36.5
    for i in range(0, 8):
        for j in range(0, 3):
            add_qr_code_image(x0 + dx * j, y0 + dy * i, img_path)


add_image_to_pdf(img_path)

pdf.output("C:/PP/DCProject/DCP/TestPart/simple_demo.pdf")
