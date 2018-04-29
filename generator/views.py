from django.http import HttpResponse
from django.shortcuts import render

import pdfkit

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
