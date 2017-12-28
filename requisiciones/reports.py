# -*- coding: utf-8 -*-
from django.conf import settings
from os.path import join
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image
from reportlab.lib.units import cm, mm
from .models import Pedido


def get_pedido_por_estado_pdf(estado):
	pedidos = Pedido.objects.filter(estado=estado)
	
	buff = BytesIO()

	doc = SimpleDocTemplate(buff,pagesize=A4,rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)
	styles = getSampleStyleSheet()	

	report = [
		Paragraph("REPORTE DE PEDIDOS POR ESTADO", styles['Title']),
		Paragraph("Estado: %s" % (dict(Pedido.ESTADO_CHOICES).get(int(estado))), styles['Heading4']),
	]

	headers = ['Código','Usuario', 'Fecha','Estado', 'Lugar']
	columns_width = [1.5*cm, 3*cm,2.3*cm,1.5*cm,4*cm, 3*cm]	
	fields = (
		{'name': 'id'},{'name': 'usuario.get_full_name'},{'name': 'fecha'},
		{'name': 'get_estado', 'kwargs': {'html': False}},
		{'name': 'lugar'},				
	)
	

	data = get_table_data(pedidos, fields)	
	data = get_styled_data([headers,] + data)	
	table = Table(data, style=get_table_style(), hAlign='LEFT')	
	
	
	report.append(table)
	doc.build(report,canvasmaker=NumberedCanvas,onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)	
	return buff.getvalue()



def get_letterhead_page(canvas, doc):
        # Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		base_path = join(settings.BASE_DIR, 'static/assets/img/')

		logo = Image(base_path + 'logo.jpg', width=5*cm,height=2.5*cm)		

		w, h = logo.wrap(doc.width, doc.topMargin)
		logo.drawOn(canvas, doc.leftMargin + 400, doc.height + doc.topMargin - 30)

        # Release the canvas
		canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(115*mm, 5*mm,
            "Página %d de %d" % (self._pageNumber, page_count))




def get_paragraph(text, size):
	style = getSampleStyleSheet()['Normal']
	style.fontSize = size
	style.leading = size

	return Paragraph(text, style=style)

def get_table_style():
	style = TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
		('GRID',(0,0),(-1,-1), 0.25, colors.black),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
		('FONTSIZE', (0, 0), (-1, -1), 6),
	])

	return style

def get_styled_data(data):
	styles = getSampleStyleSheet()

	style = styles['Heading5']
	style.fontSize = 10

	data[0] = (Paragraph(head, style) for head in data[0])
	return data

def get_attribute(instance, field):
	names = field['name'].split('.')
	name = names.pop(0)

	if len(names) == 0:
		if not name:
			return None

		attr = getattr(instance, name)
		
		if callable(attr):
			result = attr(**field['kwargs']) if 'kwargs' in field else attr()
 			return  get_paragraph(result, 8)
		
		return get_paragraph(str(attr), 8)
 	
 	_field = field.copy()
 	_field['name'] = '.'.join(names)
	return get_attribute(getattr(instance, name), _field)

def get_table_data(object_list, fields ,style=None):
	data = []	
	for obj in object_list:		
		line = [get_attribute(obj, field) for field in fields]
		data.append(line)

	return data