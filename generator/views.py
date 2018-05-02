from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from io import BytesIO

import pdfkit

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, B5, landscape
from reportlab.lib.units import mm, inch

# Create your views here.
from django.template.loader import render_to_string

from .labels import Generator, Writer, BufferedWriter

def test_pdfkit(request):
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
    
    response = HttpResponse(content_type='application/pdf')

    label_content = {
        'image': {
            'path': r'C:\Users\tpiwo\Projects\pdftest\generator\static\images\label.jpg'
        },
        'strings': {
            'product-name': 'Lorem ipsum',
            'total-fat': 10,
            'best-by-fresh': datetime.now().strftime('%Y-%m-%d'),
            'best-by-frozen': datetime.now().strftime('%Y-%m-%d')
        }
    }

    label_template = {
        'page': {
            'size': (3.5*inch, 3.5*inch)
        },
        'image': {
            'size': (3.5*inch, 3.5*inch)
        },
        'strings': {
            'product-name': {
                'position': (0.4, 0.7),
                'color': (1, 1, 1),
                'font-size': 10
            },
            'total-fat': {
                'position': (0.02, 0.45),
                'color': (0, 0, 0),
                'font-size': 6
            },
            'best-by-fresh': {
                'position': (0.6, 0.055),
                'color': (1, 1, 1),
                'font-size': 6
            },
            'best-by-frozen': {
                'position': (0.6, 0.025),
                'color': (1, 1, 1),
                'font-size': 6
            }
        }
    }

    writer = Writer(response)
    generator = Generator(label_template, writer)
    generator.draw_product_labels(label_content, 2)
    generator.end()

    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    return response
