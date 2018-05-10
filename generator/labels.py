from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, B5, landscape
from reportlab.lib.units import mm, inch

class Generator(object):
    
    def __init__(self, label_template, writer):
        self.label_template = label_template
        self.writer = writer
        self.canvas = canvas.Canvas(
            self.writer.get_output(), 
            pagesize=self.label_template['page']['size'])

    def draw_product_labels(self, label_content, labels_count):
        for i in range(0, labels_count):
            width, height = self.__calculate_position(
                *self.label_template['image']['size'])
            
            self.canvas.drawImage(
                label_content['image']['path'], 
                0, 0, width, height)

            for key, value in label_content['strings'].items():
                x, y = self.__calculate_position(
                    *self.label_template['strings'][key]['position'])
                color = self.label_template['strings'][key]['color']
                font_size = self.label_template['strings'][key]['font-size']
                self.canvas.setFillColorRGB(*color)
                self.canvas.setFontSize(font_size)                
                self.canvas.drawString(x, y, str(value))

            self.canvas.showPage()

    def __calculate_position(self, x, y):
        return (self.label_template['page']['size'][0] * x,
                self.label_template['page']['size'][1] * y)

    def end(self):
        self.canvas.save()
        self.writer.end()


class BufferedWriter(object):

    def __init__(self, output):
        self.output = output
        self.buffer = BytesIO()
    
    def get_output(self):
        return self.buffer

    def end(self):
        content = self.buffer.getvalue()
        self.buffer.close()
        self.output.write(content)


class Writer(object):

    def __init__(self, output):
        self.output = output
    
    def get_output(self):
        return self.output

    def end(self):
        pass
