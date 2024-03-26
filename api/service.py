import os
from datetime import datetime
from io import BytesIO

import pdfkit
import qrcode
from django.conf import settings
from django.http import FileResponse, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse

from rest_framework.views import APIView

from api.models import Item
from .serializers import ItemSerializer


class CashMachineService:
    template_name = "cheque.html"

    def generate_cheque_pdf(self, context, html_file_path, pdf_file_path):
        html_content = render_to_string(self.template_name, context)
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        pdfkit.from_file(html_file_path, pdf_file_path)

    def generate_qr_code(self, request, pdf_file_path):
        qr_link = request.build_absolute_uri(reverse("qrcode", kwargs={"filename": pdf_file_path.split('/')[-1]}))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_bytes_io = BytesIO()
        qr_img.save(qr_bytes_io, format='PNG')
        qr_bytes_io.seek(0)

        return qr_bytes_io

    def get_cheque_data(self, request):
        items_data = request.data.get('items', [])
        item_ids = [int(item_id) for item_id in items_data]

        items = Item.objects.filter(id__in=item_ids)
        quantity = {item.id: item_ids.count(item.id) for item in items}
        item_price = {item.id: item.price * quantity[item.id] for item in items if item.id}
        total_items = sum(quantity.values())
        total_price = sum(item.price * quantity[item.id] for item in items)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        serializer = ItemSerializer(items, many=True)
        return {
            "items": serializer.data,
            "quantity": quantity,
            "item_price": item_price,
            "total_items": total_items,
            "total_price": total_price,
            "current_time": current_time,
        }
