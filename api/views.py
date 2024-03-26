import os

from django.conf import settings
from django.http import FileResponse, JsonResponse, HttpResponse
from rest_framework.views import APIView

from .service import CashMachineService


class CashMachineAPIView(APIView):
    def post(self, request):
        try:
            context = CashMachineService().get_cheque_data(request)
            html_file_path = "media/cheque.html"
            pdf_file_path = "media/cheque.pdf"

            CashMachineService().generate_cheque_pdf(context, html_file_path, pdf_file_path)
            qr_bytes_io = CashMachineService().generate_qr_code(request, pdf_file_path)

            return FileResponse(qr_bytes_io, content_type='image/png')
        except ValueError:
            return JsonResponse({"error": "Invalid data format. Expected an array of integers."}, status=400)


class QRCodeApiView(APIView):

    def get(self, request, filename):
        cheque_pdf_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(cheque_pdf_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            return response
