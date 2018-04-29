from django.http import HttpResponse
from django.shortcuts import render

from io import BytesIO

import pdfkit

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, B5, landscape
from reportlab.lib.units import mm

# Create your views here.
from django.template.loader import render_to_string


def test(request):
    context = {
        'pages': [
            dict(number=1, text='ala ma kota'),
            dict(number=2, text='tomek ma psa'),
            dict(number=3, text='lorem ipsum')
        ]
    }
    content = render_to_string('generator/test.html', context, request)

    options = {
        'page-width': 200,
        'page-height': 220,
        'margin-left': 15,
        'margin-right': 15,
        'margin-top': 25,
        'margin-bottom': 25,
        # 'images': ''
    }

    content = pdfkit.from_string(content, output_path=False, options=options)
    return HttpResponse(content, content_type='application/pdf')

    # return render(request, 'generator/test.html', context=context)

def test_reportlab(request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    for i in range(0, 2):
        # image = Image.open(r'C:\Users\tpiwo\Projects\pdftest\generator\static\images\sample.jpg')
        pdf.setPageSize(landscape(letter))
        pdf.drawImage(r'C:\Users\tpiwo\Projects\pdftest\generator\static\images\sample.jpg', 0, 0)
        pdf.drawString(30, 100, 'lorem ipsum')
        pdf.showPage()

    pdf.save()
    content = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    response.write(content)
    return response
