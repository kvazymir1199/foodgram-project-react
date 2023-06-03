import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from django.conf import settings
from ingredients.models import Ingredient

X, Y, LINE_HEIGH = (120, 700, 20)
FONT_SIZE = 12
PDF_TITLE = "Список покупок:"
DATA_PATH = os.path.join(
    Path(settings.BASE_DIR).resolve().parent.parent,
    "data\\font\\DejaVuSansCondensed.ttf",
)


def get_pdf_file(buy_list):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont("DejaVu", DATA_PATH))
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("DejaVu", FONT_SIZE)
    y = Y
    p.drawString(X - 20, y, PDF_TITLE)
    y -= LINE_HEIGH
    for i, item in enumerate(buy_list, start=1):
        ingredient = Ingredient.objects.get(pk=item["ingredient"])
        text = (
            f'{i}: {ingredient.name}, {item["amount"]} '
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
