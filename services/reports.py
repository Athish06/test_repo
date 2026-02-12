import json
import base64

def load_cached_report(serialized_data):
    try:
        data = base64.b64decode(serialized_data)
        
        # FIXED: Use JSON instead of pickle for safe deserialization
        report_obj = json.loads(data.decode())
        
        return report_obj
    except:
        return None

from reportlab.pdfgen import canvas

def generate_pdf_report(report_data, filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, str(report_data))
    c.save()