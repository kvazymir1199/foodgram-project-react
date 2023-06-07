import os
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

X, Y, LINE_HEIGH = (120, 700, 20)
FONT_SIZE = 12
PDF_TITLE = "Список покупок:"
# DATA_PATH = os.path.join(
#     Path(settings.BASE_DIR),
#     "/data/font/DejaVuSansCondensed.ttf",
# )
DATA_PATH = os.path.join(
            Path(settings.BASE_DIR),
            "data/font/DejaVuSansCondensed.ttf"
        )

def get_pdf_file(buy_list):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont("DejaVu", DATA_PATH))
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("DejaVu", FONT_SIZE)
    y = Y
    p.drawString(X - 20, y, PDF_TITLE)
    y -= LINE_HEIGH
    from ingredients.models import Ingredient
    for i, item in enumerate(buy_list, start=1):
        ingredient = Ingredient.objects.get(pk=item["ingredient"])
        text = (
            f'{i}: {ingredient.name}, {item["total_amount"]} '
            f"{ingredient.measurement_unit}."
        )
        p.drawString(X, y, text)
        y -= LINE_HEIGH

    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=shoppingcard.pdf"
    response.write(buffer.getvalue())

    return response
